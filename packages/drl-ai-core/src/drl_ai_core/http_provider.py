"""OpenAI-compatible HTTP provider for locally hosted open-weight models.

One adapter covers every local runtime worth using — Ollama, vLLM, LM Studio, and
``llama-server`` all expose the same ``/v1/chat/completions`` shape — so the
workshop can change runtime without changing code.

Three behaviours here are deliberate rather than incidental:

**Completions are streamed, and the timeout is a stall timeout.** A single
blocking request with a wall-clock deadline is the wrong instrument for local
inference: a 26B model generating steadily on CPU is indistinguishable from a
dead endpoint until the deadline fires, and raising the deadline only makes a
genuinely dead endpoint take longer to detect. Streaming separates the two
questions. ``stall_timeout`` asks "is anything still arriving?" and fails fast
when nothing is; ``constraints.timeout_seconds`` is a runaway ceiling on the
whole call, not a guess at how long the model ought to need.

**Reasoning traces are discarded, never recorded.** Reasoning-capable models
return internal thinking either in a separate ``reasoning`` field or fenced in
``<think>`` tags. `COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md` forbids inferring or
requiring disclosure of private chain-of-thought, and the control plane records
observable state only. This provider strips thinking content before returning and
never places it in the trace. What the model concluded is observable; how it got
there is not treated as evidence.

**Open-weight enforcement is honest about what it can know.** ``open_weight`` is
declared by the caller from the model register, not sniffed from the endpoint — a
local server cannot prove the license of the weights it loaded. The flag records
what was configured, so a mislabelled register produces a wrong disclosure rather
than a silent one.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from collections.abc import Iterator, Sequence
from http.client import HTTPException, HTTPResponse
from typing import Any

from .providers import (
    ChatMessage,
    CompletionConstraints,
    ModelIdentity,
    OutputMode,
    ProviderTimeoutError,
    ProviderUnavailableError,
    StructuredModelResponse,
)

__all__ = [
    "DEFAULT_STALL_TIMEOUT_SECONDS",
    "THINKING_OFF_HINTS",
    "HttpOpenAICompatibleProvider",
    "strip_reasoning",
]

#: Fenced reasoning blocks emitted inline by some reasoning models.
_THINK_BLOCK = re.compile(r"<think>.*?</think>\s*", re.DOTALL | re.IGNORECASE)

#: Keys under which runtimes return separate reasoning content.
_REASONING_KEYS = ("reasoning", "reasoning_content", "thinking")

#: Default seconds to wait for the *next* byte before declaring the endpoint dead.
#:
#: Generous enough to cover a cold model load before the first token, tight
#: enough that a hung endpoint is caught in a minute or two rather than at the
#: end of the total budget.
DEFAULT_STALL_TIMEOUT_SECONDS = 120.0

#: Vendor hints that ask a reasoning-capable model not to think before answering.
#:
#: There is no standard for this. Ollama takes ``think``; vLLM and other
#: template-driven servers take ``chat_template_kwargs.enable_thinking``. Both are
#: sent together because a server that does not recognise a key ignores it. This
#: is a best-effort request, not a guarantee: a server that rejects unknown
#: fields will fail the call, which is why it is opt-in.
THINKING_OFF_HINTS: dict[str, Any] = {
    "think": False,
    "chat_template_kwargs": {"enable_thinking": False},
}


def strip_reasoning(text: str) -> str:
    """Remove inline reasoning blocks from model output.

    An unterminated ``<think>`` block means the model was cut off mid-reasoning
    and produced no answer; everything from the opening tag on is dropped rather
    than returned as if it were content.
    """
    cleaned = _THINK_BLOCK.sub("", text)
    lowered = cleaned.lower()
    if "<think>" in lowered:
        cleaned = cleaned[: lowered.index("<think>")]
    return cleaned.strip()


class _StreamState:
    """Accumulates a chat completion from server-sent delta chunks."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.finish_reason = ""
        self.usage: dict[str, int] = {}
        self.tool_calls: dict[int, dict[str, str]] = {}
        self.chunks = 0
        self.first_token_ms: float | None = None

    def text(self) -> str:
        return "".join(self.parts)

    def absorb(self, chunk: dict[str, Any], elapsed_ms: float) -> None:
        self.chunks += 1
        usage = chunk.get("usage")
        if isinstance(usage, dict):
            self.usage.update(_coerce_counts(usage))

        choices = chunk.get("choices")
        if not isinstance(choices, list) or not choices:
            return
        choice = choices[0]
        if not isinstance(choice, dict):
            return

        reason = choice.get("finish_reason")
        if isinstance(reason, str) and reason:
            self.finish_reason = reason

        # Some servers replay the whole message on the terminal chunk instead of
        # a delta. Either shape carries the same fields.
        delta = choice.get("delta")
        if not isinstance(delta, dict):
            delta = choice.get("message")
        if not isinstance(delta, dict):
            return

        piece = delta.get("content")
        if isinstance(piece, str) and piece:
            if self.first_token_ms is None:
                self.first_token_ms = elapsed_ms
            self.parts.append(piece)

        # Reasoning deltas are dropped on arrival, not collected and filtered
        # later: content that is never accumulated cannot leak into the trace.
        for key in _REASONING_KEYS:
            if delta.get(key) and self.first_token_ms is None:
                self.first_token_ms = elapsed_ms

        self._absorb_tool_calls(delta.get("tool_calls"))

    def _absorb_tool_calls(self, raw: Any) -> None:
        if not isinstance(raw, list):
            return
        for position, call in enumerate(raw):
            if not isinstance(call, dict):
                continue
            index = call.get("index")
            slot = index if isinstance(index, int) else position
            function = call.get("function")
            if not isinstance(function, dict):
                continue
            entry = self.tool_calls.setdefault(slot, {"name": "", "arguments": ""})
            name = function.get("name")
            if isinstance(name, str) and name:
                entry["name"] = name
            arguments = function.get("arguments")
            if isinstance(arguments, str):
                # Arguments arrive as a JSON string split across chunks.
                entry["arguments"] += arguments


def _coerce_counts(raw: dict[str, Any]) -> dict[str, int]:
    return {
        key: int(value)
        for key, value in raw.items()
        if isinstance(value, int | float) and not isinstance(value, bool)
    }


class HttpOpenAICompatibleProvider:
    """Talk to a local OpenAI-compatible chat completions endpoint."""

    def __init__(
        self,
        *,
        model: str,
        base_url: str = "http://localhost:11434/v1",
        provider_id: str = "local-openai-compatible",
        model_family: str = "",
        revision: str = "",
        license_label: str = "unreviewed",
        open_weight: bool = True,
        quantization: str | None = None,
        runtime: str = "ollama",
        api_key: str | None = None,
        connect_timeout: float = 5.0,
        stream: bool = True,
        stall_timeout: float = DEFAULT_STALL_TIMEOUT_SECONDS,
        extra_payload: dict[str, Any] | None = None,
    ) -> None:
        if stall_timeout <= 0:
            raise ValueError("stall_timeout must be positive")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.connect_timeout = connect_timeout
        self.stream = stream
        self.stall_timeout = stall_timeout
        self.extra_payload = dict(extra_payload or {})
        self._identity = ModelIdentity(
            provider_id=provider_id,
            model_family=model_family or model,
            # Absent an explicit pin, record the tag actually requested rather
            # than a placeholder, so a report cannot claim more precision than
            # the run had.
            revision=revision or model,
            open_weight=open_weight,
            output_mode=OutputMode.LIVE,
            license_label=license_label,
            quantization=quantization,
            runtime=runtime,
        )

    @property
    def identity(self) -> ModelIdentity:
        return self._identity

    def _url(self, path: str) -> str:
        url = f"{self.base_url}{path}"
        if not url.startswith(("http://localhost", "http://127.0.0.1", "https://")):
            raise ProviderUnavailableError(f"refusing non-local plaintext endpoint: {url}")
        return url

    def _request(self, url: str, payload: dict[str, Any]) -> urllib.request.Request:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return urllib.request.Request(  # noqa: S310 - scheme checked in _url
            url, data=json.dumps(payload).encode(), headers=headers
        )

    def _open(self, url: str, payload: dict[str, Any], timeout: float) -> HTTPResponse:
        """Open the connection, translating transport failures into provider errors."""
        request = self._request(url, payload)
        try:
            # The scheme is validated in _url: only loopback HTTP or HTTPS
            # reaches this call, so file:// and custom schemes cannot.
            response: HTTPResponse = urllib.request.urlopen(  # noqa: S310  # nosec B310
                request, timeout=timeout
            )
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:300]
            raise ProviderUnavailableError(f"endpoint returned HTTP {exc.code}: {detail}") from exc
        except TimeoutError as exc:
            raise ProviderTimeoutError(
                f"no response from {url} within {timeout:.0f}s"
            ) from exc
        except (urllib.error.URLError, OSError, HTTPException) as exc:
            reason = getattr(exc, "reason", exc)
            if isinstance(reason, TimeoutError):
                raise ProviderTimeoutError(
                    f"no response from {url} within {timeout:.0f}s"
                ) from exc
            raise ProviderUnavailableError(f"cannot reach {url}: {reason}") from exc
        return response

    def _post(self, path: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
        """Send one non-streaming request and return the decoded JSON object."""
        url = self._url(path)
        with self._open(url, payload, timeout) as response:
            try:
                body = response.read().decode("utf-8", "replace")
            except (TimeoutError, OSError, HTTPException) as exc:
                raise self._read_failure(url, exc, timeout) from exc
        return _decode_object(body)

    def _read_failure(
        self, url: str, exc: BaseException, timeout: float
    ) -> ProviderTimeoutError | ProviderUnavailableError:
        reason = getattr(exc, "reason", exc)
        if isinstance(exc, TimeoutError) or isinstance(reason, TimeoutError):
            return ProviderTimeoutError(f"{url} stalled: no data for {timeout:.0f}s")
        return ProviderUnavailableError(f"connection to {url} failed mid-response: {reason}")

    def _stream_lines(
        self, url: str, payload: dict[str, Any], deadline: float
    ) -> Iterator[bytes]:
        """Yield raw response lines, enforcing stall and total-time limits.

        The socket timeout is a *per-read* limit, so it is exactly a stall
        detector: it fires when no byte has arrived for ``stall_timeout``, not
        when the whole generation has taken too long. The deadline check between
        lines supplies the separate runaway ceiling.
        """
        with self._open(url, payload, self.stall_timeout) as response:
            while True:
                try:
                    line = response.readline()
                except (TimeoutError, OSError, HTTPException) as exc:
                    raise self._read_failure(url, exc, self.stall_timeout) from exc
                if not line:
                    return
                if time.monotonic() > deadline:
                    raise ProviderTimeoutError(
                        f"exceeded the total budget for {url} while still receiving output"
                    )
                yield line

    def _stream(
        self, path: str, payload: dict[str, Any], total_timeout: float
    ) -> tuple[_StreamState, float]:
        """Consume a server-sent-event completion stream into accumulated state."""
        url = self._url(path)
        started = time.perf_counter()
        deadline = time.monotonic() + total_timeout
        state = _StreamState()
        buffered: list[str] = []

        for raw in self._stream_lines(url, payload, deadline):
            line = raw.decode("utf-8", "replace").strip()
            if not line or line.startswith(":"):
                continue
            if not line.startswith("data:"):
                # The server ignored `stream` and is sending a plain JSON body.
                buffered.append(line)
                continue
            data = line[len("data:") :].strip()
            if data == "[DONE]":
                break
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue
            if isinstance(chunk, dict):
                if _error_of(chunk):
                    raise ProviderUnavailableError(f"endpoint reported: {_error_of(chunk)}")
                state.absorb(chunk, (time.perf_counter() - started) * 1000)

        if not state.chunks and buffered:
            state.absorb(_decode_object("".join(buffered)), (time.perf_counter() - started) * 1000)
        if not state.chunks:
            raise ProviderUnavailableError(f"{url} closed the stream without sending any data")
        return state, (time.perf_counter() - started) * 1000

    def health(self) -> bool:
        """Probe the endpoint. Never raises — an unhealthy provider is a False."""
        try:
            self._post(
                "/chat/completions",
                {
                    "model": self.model,
                    "messages": [{"role": "user", "content": "ping"}],
                    "max_tokens": 1,
                    "stream": False,
                },
                timeout=self.connect_timeout,
            )
        except (ProviderUnavailableError, ProviderTimeoutError):
            return False
        return True

    def _payload(
        self,
        messages: Sequence[ChatMessage],
        tools: Sequence[dict[str, Any]] | None,
        constraints: CompletionConstraints,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": constraints.temperature,
            "max_tokens": constraints.max_output_tokens,
            "stream": self.stream,
        }
        if self.stream:
            # Token counts otherwise vanish in streaming mode; servers that do
            # not know the option ignore it.
            payload["stream_options"] = {"include_usage": True}
        if tools:
            payload["tools"] = list(tools)
        payload.update(self.extra_payload)
        return payload

    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        tools: Sequence[dict[str, Any]] | None = None,
        constraints: CompletionConstraints,
    ) -> StructuredModelResponse:
        if not messages:
            raise ValueError("messages cannot be empty")
        if constraints.require_open_weight and not self._identity.open_weight:
            raise ProviderUnavailableError(
                f"provider {self._identity.provider_id!r} is not registered as open-weight"
            )

        payload = self._payload(messages, tools, constraints)
        if self.stream:
            return self._complete_streaming(payload, constraints)
        return self._complete_blocking(payload, constraints)

    def _complete_streaming(
        self, payload: dict[str, Any], constraints: CompletionConstraints
    ) -> StructuredModelResponse:
        state, latency_ms = self._stream(
            "/chat/completions", payload, constraints.timeout_seconds
        )
        return StructuredModelResponse(
            content=strip_reasoning(state.text()),
            identity=self._identity,
            finish_reason=state.finish_reason or "stop",
            latency_ms=latency_ms,
            usage=state.usage,
            tool_calls=tuple(
                {"name": call["name"], "arguments": call["arguments"]}
                for _, call in sorted(state.tool_calls.items())
            ),
            transport={
                "streamed": True,
                "chunks": state.chunks,
                "first_token_ms": state.first_token_ms,
            },
        )

    def _complete_blocking(
        self, payload: dict[str, Any], constraints: CompletionConstraints
    ) -> StructuredModelResponse:
        started = time.perf_counter()
        body = self._post("/chat/completions", payload, timeout=constraints.timeout_seconds)
        latency_ms = (time.perf_counter() - started) * 1000

        choices = body.get("choices") or []
        if not choices or not isinstance(choices[0], dict):
            raise ProviderUnavailableError("endpoint returned no choices")
        choice = choices[0]
        message = choice.get("message") or {}

        content = strip_reasoning(str(message.get("content") or ""))
        # Reasoning arrives either fenced inline or in a side channel. Both are
        # dropped here; neither reaches the caller or the trace.
        for key in _REASONING_KEYS:
            message.pop(key, None)

        tool_calls: list[dict[str, Any]] = []
        for call in message.get("tool_calls") or []:
            if not isinstance(call, dict):
                continue
            function = call.get("function") or {}
            tool_calls.append(
                {
                    "name": str(function.get("name", "")),
                    "arguments": function.get("arguments", ""),
                }
            )

        return StructuredModelResponse(
            content=content,
            identity=self._identity,
            finish_reason=str(choice.get("finish_reason") or "stop"),
            latency_ms=latency_ms,
            usage=_coerce_counts(body.get("usage") or {}),
            tool_calls=tuple(tool_calls),
            transport={"streamed": False, "chunks": 1, "first_token_ms": latency_ms},
        )


def _error_of(chunk: dict[str, Any]) -> str:
    """Return an error message carried inside a stream chunk, if any."""
    error = chunk.get("error")
    if isinstance(error, dict):
        return str(error.get("message") or error)[:300]
    if isinstance(error, str) and error:
        return error[:300]
    return ""


def _decode_object(body: str) -> dict[str, Any]:
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ProviderUnavailableError(f"endpoint returned non-JSON: {body[:200]}") from exc
    if not isinstance(parsed, dict):
        raise ProviderUnavailableError("endpoint returned a non-object response")
    return parsed
