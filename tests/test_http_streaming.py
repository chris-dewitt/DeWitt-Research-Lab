"""Tests for the streaming HTTP provider against a real loopback endpoint.

These run a live socket rather than patching ``urlopen``. The behaviour under
test *is* the transport — SSE framing, when the socket times out, what happens
when a server closes mid-stream — and a mock of ``urlopen`` would assert only
that the mock behaves as written.

The load-bearing claim is that the timeout is a stall timeout: a model that
generates steadily for longer than the timeout must succeed, and a model that
goes silent for longer than the timeout must fail. A wall-clock deadline cannot
tell those apart, which is why one existed and the endpoint kept "timing out".
"""

from __future__ import annotations

import contextlib
import importlib.util
import json
import sys
import threading
import time
from collections.abc import Callable, Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest import mock

import pytest
from drl_ai_core.http_provider import THINKING_OFF_HINTS, HttpOpenAICompatibleProvider
from drl_ai_core.providers import (
    ChatMessage,
    CompletionConstraints,
    ProviderTimeoutError,
    ProviderUnavailableError,
)

Responder = Callable[[BaseHTTPRequestHandler], None]


@contextlib.contextmanager
def local_endpoint(responder: Responder) -> Iterator[tuple[str, list[dict[str, Any]]]]:
    """Serve one scripted response on loopback; yield its base URL and requests seen."""
    recorded: list[dict[str, Any]] = []

    class Handler(BaseHTTPRequestHandler):
        # HTTP/1.0 so closing the connection is what ends the body, which is
        # exactly how a streaming endpoint signals completion.
        protocol_version = "HTTP/1.0"

        def log_message(self, *args: Any) -> None:  # keep test output clean
            return

        def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler contract
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length)
            recorded.append(json.loads(body or b"{}"))
            with contextlib.suppress(BrokenPipeError, ConnectionResetError):
                responder(self)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/v1", recorded
    finally:
        server.shutdown()
        server.server_close()


def sse(
    chunks: list[dict[str, Any]],
    *,
    delay: float = 0.0,
    hang_after: float = 0.0,
    done: bool = True,
) -> Responder:
    """Respond with a server-sent-event stream of chat completion chunks."""

    def respond(handler: BaseHTTPRequestHandler) -> None:
        handler.send_response(200)
        handler.send_header("Content-Type", "text/event-stream")
        handler.end_headers()
        for chunk in chunks:
            handler.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode())
            handler.wfile.flush()
            if delay:
                time.sleep(delay)
        if hang_after:
            time.sleep(hang_after)
        if done:
            handler.wfile.write(b"data: [DONE]\n\n")
            handler.wfile.flush()

    return respond


def plain_json(body: dict[str, Any]) -> Responder:
    """Respond with an ordinary JSON body, ignoring the stream flag."""

    def respond(handler: BaseHTTPRequestHandler) -> None:
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(body).encode())
        handler.wfile.flush()

    return respond


def text_delta(content: str, **extra: Any) -> dict[str, Any]:
    return {"choices": [{"index": 0, "delta": {"content": content, **extra}}]}


def finish(reason: str = "stop") -> dict[str, Any]:
    return {"choices": [{"index": 0, "delta": {}, "finish_reason": reason}]}


PLAN = '{"task_id": "t1", "steps": []}'


def provider_at(base_url: str, **kwargs: Any) -> HttpOpenAICompatibleProvider:
    kwargs.setdefault("stall_timeout", 2.0)
    return HttpOpenAICompatibleProvider(model="test-model", base_url=base_url, **kwargs)


def ask(
    provider: HttpOpenAICompatibleProvider, *, timeout: float = 30.0
) -> Any:
    return provider.complete(
        [ChatMessage(role="user", content="plan this")],
        constraints=CompletionConstraints(timeout_seconds=timeout),
    )


class TestStreamAccumulation:
    def test_deltas_are_joined_in_order(self) -> None:
        chunks = [text_delta(piece) for piece in ('{"task_id"', ': "t1", ', '"steps": []}')]
        with local_endpoint(sse([*chunks, finish()])) as (url, _):
            response = ask(provider_at(url))
        assert response.content == PLAN
        assert response.finish_reason == "stop"

    def test_transport_records_first_token_and_chunk_count(self) -> None:
        """Time to first token and total time are different faults; report both."""
        with local_endpoint(sse([text_delta(PLAN), finish()])) as (url, _):
            response = ask(provider_at(url))
        assert response.transport["streamed"] is True
        assert response.transport["chunks"] == 2
        assert response.transport["first_token_ms"] is not None
        assert response.transport["first_token_ms"] <= response.latency_ms

    def test_usage_from_the_terminal_chunk_is_kept(self) -> None:
        usage = {"prompt_tokens": 412, "completion_tokens": 37, "total_tokens": 449}
        with local_endpoint(sse([text_delta(PLAN), {"usage": usage, "choices": []}])) as (
            url,
            _,
        ):
            response = ask(provider_at(url))
        assert response.usage == usage

    def test_a_server_that_ignores_the_stream_flag_still_works(self) -> None:
        """Not every local runtime honours `stream`; a plain body must not be lost."""
        body = {
            "choices": [{"message": {"content": PLAN}, "finish_reason": "stop"}],
            "usage": {"completion_tokens": 12},
        }
        with local_endpoint(plain_json(body)) as (url, _):
            response = ask(provider_at(url))
        assert response.content == PLAN
        assert response.usage == {"completion_tokens": 12}

    def test_tool_call_arguments_are_reassembled_across_chunks(self) -> None:
        pieces = ['{"query"', ': "cpi"', "}"]
        chunks = [
            {
                "choices": [
                    {
                        "delta": {
                            "tool_calls": [
                                {"index": 0, "function": {"name": "atlas", "arguments": ""}}
                            ]
                        }
                    }
                ]
            }
        ]
        chunks += [
            {"choices": [{"delta": {"tool_calls": [{"index": 0, "function": {"arguments": p}}]}}]}
            for p in pieces
        ]
        with local_endpoint(sse([*chunks, finish("tool_calls")])) as (url, _):
            response = ask(provider_at(url))
        assert response.tool_calls == (
            {"name": "atlas", "arguments": '{"query": "cpi"}'},
        )


class TestReasoningIsNeverAccumulated:
    def test_side_channel_reasoning_deltas_are_dropped(self) -> None:
        chunks = [
            {"choices": [{"delta": {"reasoning_content": "first I should..."}}]},
            {"choices": [{"delta": {"thinking": "...consider the catalog"}}]},
            text_delta(PLAN),
            finish(),
        ]
        with local_endpoint(sse(chunks)) as (url, _):
            response = ask(provider_at(url))
        assert response.content == PLAN
        assert "consider" not in response.content

    def test_inline_think_block_is_stripped_from_the_assembled_text(self) -> None:
        chunks = [
            text_delta("<think>the objective mentions"),
            text_delta(" inflation</think>"),
            text_delta(PLAN),
            finish(),
        ]
        with local_endpoint(sse(chunks)) as (url, _):
            response = ask(provider_at(url))
        assert response.content == PLAN

    def test_reasoning_still_counts_as_first_token(self) -> None:
        """The model is alive once anything arrives, thinking included."""
        chunks = [{"choices": [{"delta": {"reasoning": "hmm"}}]}, text_delta(PLAN), finish()]
        with local_endpoint(sse(chunks)) as (url, _):
            response = ask(provider_at(url))
        assert response.transport["first_token_ms"] is not None


class TestTheTimeoutIsAStallTimeout:
    def test_steady_output_outlives_the_stall_timeout(self) -> None:
        """The whole point: slow is not dead.

        Six chunks 50ms apart run 300ms — well past the 200ms stall timeout —
        and must succeed, because no single gap exceeds it. A wall-clock
        deadline of the same length would have killed this run.
        """
        chunks = [text_delta(c) for c in "{}"] + [text_delta(PLAN), finish()]
        with local_endpoint(sse(chunks, delay=0.05)) as (url, _):
            response = ask(provider_at(url, stall_timeout=0.2), timeout=30.0)
        assert response.content.endswith("}")

    def test_silence_past_the_stall_timeout_fails(self) -> None:
        with local_endpoint(sse([text_delta("{")], hang_after=2.0)) as (url, _):
            with pytest.raises(ProviderTimeoutError, match="stalled"):
                ask(provider_at(url, stall_timeout=0.3), timeout=30.0)

    def test_the_total_budget_still_caps_a_runaway_generation(self) -> None:
        """Stall detection is not a licence to generate forever."""
        chunks = [text_delta("x") for _ in range(50)]
        with local_endpoint(sse(chunks, delay=0.05)) as (url, _):
            with pytest.raises(ProviderTimeoutError, match="total budget"):
                ask(provider_at(url, stall_timeout=5.0), timeout=0.3)

    def test_a_dead_port_is_unavailable_not_timed_out(self) -> None:
        """Connection refused is a different fault from silence, and reads as one."""
        provider = provider_at("http://127.0.0.1:1/v1")
        with pytest.raises(ProviderUnavailableError, match="cannot reach"):
            ask(provider, timeout=5.0)


class TestStreamFailuresAreLegible:
    def test_an_error_chunk_is_surfaced(self) -> None:
        error = {"error": {"message": 'model "test-model" not found, try pulling it'}}
        with local_endpoint(sse([error])) as (url, _):
            with pytest.raises(ProviderUnavailableError, match="not found"):
                ask(provider_at(url))

    def test_a_stream_that_sends_nothing_is_reported_as_such(self) -> None:
        with local_endpoint(sse([], done=False)) as (url, _):
            with pytest.raises(ProviderUnavailableError, match="without sending any data"):
                ask(provider_at(url))

    def test_http_error_status_carries_the_body(self) -> None:
        def respond(handler: BaseHTTPRequestHandler) -> None:
            handler.send_response(404)
            handler.end_headers()
            handler.wfile.write(b'{"error":"model not found"}')

        with local_endpoint(respond) as (url, _):
            with pytest.raises(ProviderUnavailableError, match="HTTP 404"):
                ask(provider_at(url))


class TestRequestShape:
    def test_streaming_requests_ask_for_usage(self) -> None:
        with local_endpoint(sse([text_delta(PLAN), finish()])) as (url, seen):
            ask(provider_at(url))
        assert seen[0]["stream"] is True
        assert seen[0]["stream_options"] == {"include_usage": True}

    def test_thinking_hints_are_sent_only_when_requested(self) -> None:
        with local_endpoint(sse([text_delta(PLAN), finish()])) as (url, seen):
            ask(provider_at(url))
            ask(provider_at(url, extra_payload=dict(THINKING_OFF_HINTS)))
        assert "think" not in seen[0]
        assert seen[1]["think"] is False
        assert seen[1]["chat_template_kwargs"] == {"enable_thinking": False}

    def test_blocking_mode_remains_available(self) -> None:
        body = {"choices": [{"message": {"content": PLAN}, "finish_reason": "stop"}]}
        with local_endpoint(plain_json(body)) as (url, seen):
            response = ask(provider_at(url, stream=False))
        assert seen[0]["stream"] is False
        assert response.transport["streamed"] is False
        assert response.content == PLAN

    def test_remote_plaintext_is_refused_before_any_socket_is_opened(self) -> None:
        provider = HttpOpenAICompatibleProvider(
            model="m", base_url="http://example.invalid/v1"
        )
        with pytest.raises(ProviderUnavailableError, match="non-local plaintext"):
            ask(provider)


def load_probe() -> Any:
    """Load scripts/probe_model.py as a module."""
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "probe_model", root / "scripts" / "probe_model.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["probe_model"] = module
    spec.loader.exec_module(module)
    return module


def health_then_stream(chunks: list[dict[str, Any]]) -> Responder:
    """Answer the one-token health probe, then stream the real completion."""
    calls = {"n": 0}

    def respond(handler: BaseHTTPRequestHandler) -> None:
        calls["n"] += 1
        if calls["n"] == 1:
            plain_json({"choices": [{"message": {"content": "ok"}}]})(handler)
        else:
            sse(chunks)(handler)

    return respond


class TestProbeScript:
    """A diagnostic that is itself broken is worse than none.

    The probe exists so a failing endpoint reports which stage failed. Each test
    here pins one stage's verdict, including the exit status the operator reads.
    """

    def _run(self, module: Any, url: str, *extra: str) -> int:
        argv = ["probe_model", "--base-url", url, "--stall-timeout", "3", "--timeout", "20"]
        with mock.patch.object(sys, "argv", [*argv, *extra]):
            return int(module.main())

    def test_reports_success_on_a_valid_plan(self, capsys: Any) -> None:
        module = load_probe()
        plan = json.dumps(
            {
                "task_id": "model-probe",
                "steps": [
                    {"tool_name": "atlas.research_snapshot", "arguments": {}, "risk_tier": 1}
                ],
            }
        )
        with local_endpoint(health_then_stream([text_delta(plan), finish()])) as (url, _):
            code = self._run(module, url)
        assert code == 0
        assert "1/1 steps" in capsys.readouterr().out

    def test_names_the_empty_completion_and_the_fix(self, capsys: Any) -> None:
        """All budget spent thinking is the hypothesis this probe exists to test."""
        module = load_probe()
        chunks = [{"choices": [{"delta": {"reasoning": "..."}}]}, finish("length")]
        with local_endpoint(health_then_stream(chunks)) as (url, _):
            code = self._run(module, url)
        out = capsys.readouterr().out
        assert code == 1
        assert "empty completion" in out
        assert "--no-thinking" in out

    def test_distinguishes_a_schema_failure_from_a_transport_failure(self, capsys: Any) -> None:
        module = load_probe()
        chunks = [text_delta("Sure! Here is the plan you asked for."), finish()]
        with local_endpoint(health_then_stream(chunks)) as (url, _):
            code = self._run(module, url)
        out = capsys.readouterr().out
        assert code == 1
        assert "FAILED at plan schema" in out

    def test_unreachable_endpoint_stops_at_stage_one(self, capsys: Any) -> None:
        module = load_probe()
        code = self._run(module, "http://127.0.0.1:1/v1")
        out = capsys.readouterr().out
        assert code == 1
        assert "FAILED at reachability" in out
