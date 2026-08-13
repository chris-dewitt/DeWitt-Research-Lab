#!/usr/bin/env python3
"""Diagnose a local model endpoint before wiring it behind Atticus.

Running the demo and reading which planner produced the plan tells you *that*
the model call failed. It does not tell you why, and the answers are different:
a runtime that is not listening, a model tag that is not pulled, a model that
generates too slowly to be useful, and a model that generates fine but will not
emit schema-valid JSON are four separate problems.

This walks the same path the planner takes, one stage at a time, and reports the
first stage that fails along with the number that explains it.

    python scripts/probe_model.py                       # defaults + env vars
    python scripts/probe_model.py --model gemma4:26b
    python scripts/probe_model.py --no-thinking         # ask it not to reason first

Exit status is 0 only when the endpoint returned a plan the control plane would
actually have used.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from atticus_control_plane.model_planner import build_planning_messages  # noqa: E402
from atticus_control_plane.runtime import (  # noqa: E402
    DEFAULT_MODEL_BASE_URL,
    DEFAULT_MODEL_TIMEOUT_SECONDS,
    build_local_runtime,
)
from atticus_control_plane.structured_plans import (  # noqa: E402
    build_tool_plan_validator,
)
from drl_ai_core.http_provider import (  # noqa: E402
    DEFAULT_STALL_TIMEOUT_SECONDS,
    THINKING_OFF_HINTS,
    HttpOpenAICompatibleProvider,
)
from drl_ai_core.providers import (  # noqa: E402
    ChatMessage,
    CompletionConstraints,
    ProviderError,
    StructuredModelResponse,
)
from drl_protocol import TaskRequest  # noqa: E402

PROBE_OBJECTIVE = (
    "Using the latest available public inflation evidence and Federal Reserve "
    "communication, construct a plausible synthetic bear-steepener scenario "
    "and analyze its impact on the sample regional bank."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--model",
        default=os.environ.get("ATTICUS_MODEL", "").strip() or "gemma4:26b",
        help="Model tag as the runtime knows it (default: $ATTICUS_MODEL)",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("ATTICUS_MODEL_BASE_URL", "").strip() or DEFAULT_MODEL_BASE_URL,
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_MODEL_TIMEOUT_SECONDS,
        help="Total ceiling for the planning call, in seconds",
    )
    parser.add_argument(
        "--stall-timeout",
        type=float,
        default=DEFAULT_STALL_TIMEOUT_SECONDS,
        help="Seconds of silence tolerated before the endpoint is called dead",
    )
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument(
        "--no-stream", action="store_true", help="Use one blocking request instead"
    )
    parser.add_argument(
        "--no-thinking",
        action="store_true",
        help="Ask a reasoning-capable model to answer without thinking first",
    )
    parser.add_argument("--objective", default=PROBE_OBJECTIVE)
    return parser


def _line(label: str, value: object) -> None:
    print(f"  {label:<22} {value}")


def _fail(stage: str, detail: str, *, fix: str) -> int:
    print(f"\nFAILED at {stage}")
    print(f"  {detail}")
    print(f"\nTry: {fix}")
    return 1


def stage_reachable(provider: HttpOpenAICompatibleProvider, base_url: str) -> bool:
    """Can we open a connection and get a response to a one-token request?"""
    print("[1/3] endpoint reachable")
    started = time.perf_counter()
    healthy = provider.health()
    elapsed = time.perf_counter() - started
    _line("url", f"{base_url}/chat/completions")
    _line("responded in", f"{elapsed:.2f}s")
    _line("result", "ok" if healthy else "no usable response")
    return healthy


def stage_generate(
    provider: HttpOpenAICompatibleProvider,
    messages: list[ChatMessage],
    constraints: CompletionConstraints,
) -> StructuredModelResponse | None:
    """Does the model actually generate, and how fast?"""
    print("\n[2/3] generation")
    try:
        response = provider.complete(messages, constraints=constraints)
    except ProviderError as exc:
        _line("result", f"error: {exc}")
        return None

    transport = response.transport
    first_token = transport.get("first_token_ms")
    _line("streamed", transport.get("streamed"))
    _line("chunks", transport.get("chunks"))
    _line(
        "first token after",
        f"{first_token / 1000:.2f}s" if isinstance(first_token, int | float) else "n/a",
    )
    _line("total", f"{response.latency_ms / 1000:.2f}s")
    _line("finish_reason", response.finish_reason)
    completion = response.usage.get("completion_tokens")
    if completion:
        _line("completion tokens", completion)
        if response.latency_ms > 0:
            _line("tokens/sec", f"{completion / (response.latency_ms / 1000):.1f}")
    _line("content chars", len(response.content))
    return response


def stage_schema(content: str) -> dict[str, Any] | None:
    """Would the control plane accept what came back as a plan?"""
    print("\n[3/3] plan schema")
    result = build_tool_plan_validator().parse(content)
    if not result.ok:
        _line("result", "rejected")
        for issue in result.issues:
            _line("", f"{issue.path or '<root>'}: {issue.message}")
        return None
    _line("result", "accepted")
    return result.data if isinstance(result.data, dict) else {}


def main() -> int:
    args = build_parser().parse_args()
    catalog = build_local_runtime().registry.catalog()

    provider = HttpOpenAICompatibleProvider(
        model=args.model,
        base_url=args.base_url,
        provider_id=f"local::{args.model}",
        model_family=args.model.split(":", 1)[0],
        stream=not args.no_stream,
        stall_timeout=args.stall_timeout,
        extra_payload=dict(THINKING_OFF_HINTS) if args.no_thinking else None,
    )
    constraints = CompletionConstraints(
        temperature=0.0,
        max_output_tokens=args.max_tokens,
        require_open_weight=True,
        timeout_seconds=args.timeout,
    )

    print(f"probing {args.model} at {args.base_url}")
    print(f"stall timeout {args.stall_timeout:.0f}s / total {args.timeout:.0f}s\n")

    if not stage_reachable(provider, args.base_url):
        return _fail(
            "reachability",
            "the endpoint did not answer a one-token request",
            fix=(
                "confirm the runtime is up (`ollama ps`) and that the model tag is "
                "pulled (`ollama list`). If it is served elsewhere, pass --base-url."
            ),
        )

    request = TaskRequest(
        task_id="model-probe",
        objective=args.objective,
        public_session=False,
        as_of="2026-07-24",
    )
    response = stage_generate(
        provider, build_planning_messages(request, catalog), constraints
    )
    if response is None:
        return _fail(
            "generation",
            "the model did not return a completion within budget",
            fix=(
                "a stall means nothing arrived at all — check the server log. If the "
                "total ceiling was hit while output was still arriving, the model is "
                "simply slow: raise --timeout, or use a smaller model."
            ),
        )

    if not response.content.strip():
        return _fail(
            "generation",
            f"empty completion after reasoning was stripped "
            f"(finish_reason={response.finish_reason})",
            fix=(
                "the model spent its whole budget thinking. Re-run with "
                "--no-thinking, or raise --max-tokens."
            ),
        )

    payload = stage_schema(response.content)
    if payload is None:
        print("\n  --- what came back ---")
        print(f"  {response.content[:600]}")
        return _fail(
            "plan schema",
            "the completion was not a valid plan",
            fix=(
                "this model will not hold the JSON contract at this size. Try a "
                "larger model, or an instruct variant tuned for structured output."
            ),
        )

    steps = payload.get("steps") or []
    known = {tool.name for tool in catalog}
    print("\nPLAN")
    for step in steps if isinstance(steps, list) else []:
        if not isinstance(step, dict):
            continue
        name = str(step.get("tool_name", ""))
        mark = "ok " if name in known else "DROPPED (not in registry)"
        print(f"  {mark} {name}")
    print(f"\nusable: {sum(1 for s in steps if _names_known(s, known))}/{len(steps)} steps")
    print(json.dumps(payload, indent=2))
    return 0


def _names_known(step: object, known: set[str]) -> bool:
    return isinstance(step, dict) and str(step.get("tool_name", "")) in known


if __name__ == "__main__":
    raise SystemExit(main())
