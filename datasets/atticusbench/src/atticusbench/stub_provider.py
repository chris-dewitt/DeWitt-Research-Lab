"""A provider that is not a model, for exercising the model path without one.

CI has no model daemon, and neither does a fresh clone. Without this, the only
way to know whether the model path works would be to have a model, which means
the path would be untested exactly when someone is setting it up.

This is **not a baseline and not a model**. It emits a fixed plan shape from the
offered catalog with no understanding of the request, so its scores are
meaningless as a measurement. It exists to prove the plumbing: that a completion
is parsed, that an unknown tool is dropped, that a claimed tier is replaced, and
that a malformed completion produces no plan rather than a fallback one.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from typing import Any

from drl_ai_core.providers import (
    ChatMessage,
    CompletionConstraints,
    ModelIdentity,
    OutputMode,
    StructuredModelResponse,
)

#: What a stub is, spelled out where it will be read back off a record.
STUB_LICENSE_LABEL = "not-a-model"


def first_tool_plan(messages: Sequence[ChatMessage]) -> str:
    """Name the first catalog tool with no arguments.

    Deliberately naive: it produces argument-contract violations on most cases,
    which is a useful shakedown of the failure paths and is not a capability.
    """

    task_id = _task_id(messages)
    tools = _catalog_names(messages)
    if not tools:
        return json.dumps({"task_id": task_id, "steps": []})
    return json.dumps(
        {
            "task_id": task_id,
            "steps": [{"tool_name": tools[0], "arguments": {}, "risk_tier": 1}],
        }
    )


def empty_plan(messages: Sequence[ChatMessage]) -> str:
    """Always abstain."""

    return json.dumps({"task_id": _task_id(messages), "steps": []})


def hallucinating_plan(messages: Sequence[ChatMessage]) -> str:
    """Name a tool that is not in the catalog, and claim tier zero for it."""

    return json.dumps(
        {
            "task_id": _task_id(messages),
            "steps": [
                {"tool_name": "nonexistent.tool", "arguments": {}, "risk_tier": 0},
            ],
        }
    )


def prose_plan(messages: Sequence[ChatMessage]) -> str:
    """Return something that is not a plan at all."""

    del messages
    return "Sure! I would start by looking at the repository status, and then..."


def _task_id(messages: Sequence[ChatMessage]) -> str:
    for message in messages:
        for line in message.content.splitlines():
            if line.startswith("task_id: "):
                return line.removeprefix("task_id: ").strip()
    return "unknown"


def _catalog_names(messages: Sequence[ChatMessage]) -> list[str]:
    names: list[str] = []
    for message in messages:
        for line in message.content.splitlines():
            if not line.startswith("- "):
                continue
            candidate = line.removeprefix("- ").split(" ", 1)[0]
            if "." in candidate:
                names.append(candidate)
    return names


class StubPlanProvider:
    """Deterministic provider whose completion is computed from the prompt."""

    def __init__(
        self,
        responder: Callable[[Sequence[ChatMessage]], str] = first_tool_plan,
        *,
        provider_id: str = "stub-plan",
        healthy: bool = True,
        raises: Exception | None = None,
    ) -> None:
        self._responder = responder
        self._healthy = healthy
        self._raises = raises
        self._identity = ModelIdentity(
            provider_id=provider_id,
            model_family="atticusbench-stub",
            revision="stub-1",
            # True so the open-weight constraint does not reject it. Nothing
            # here is a weight of any kind; the license label says so.
            open_weight=True,
            output_mode=OutputMode.LIVE,
            license_label=STUB_LICENSE_LABEL,
            runtime="stub",
        )

    @property
    def identity(self) -> ModelIdentity:
        return self._identity

    def health(self) -> bool:
        return self._healthy

    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        tools: Sequence[dict[str, Any]] | None = None,
        constraints: CompletionConstraints,
    ) -> StructuredModelResponse:
        del tools, constraints
        if self._raises is not None:
            raise self._raises
        content = self._responder(messages)
        return StructuredModelResponse(
            content=content,
            identity=self._identity,
            finish_reason="stop",
            latency_ms=0.0,
            usage={"prompt_tokens": 0, "completion_tokens": 0},
        )
