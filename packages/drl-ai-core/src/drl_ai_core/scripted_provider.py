"""A provider that replays scripted answers, for exercising the bake-off harness.

:class:`~drl_ai_core.mock_provider.MockOpenWeightProvider` returns one canned
shape regardless of input, which is right for gateway tests and useless for a
bake-off — every candidate would score identically. This provider maps task ids
to specific responses, so a fixture bake-off can produce *differentiated* results
and the harness's ranking, margin, and gate logic can be tested against known
inputs.

It is a test and demonstration instrument. It performs no inference and must
never stand in for a real candidate in evidence offered to DIR-004; runs driven
by it are tagged ``measurement_mode="fixture"``, which the evidence gate rejects
for selection.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .providers import (
    ChatMessage,
    CompletionConstraints,
    ModelIdentity,
    OutputMode,
    ProviderUnavailableError,
    StructuredModelResponse,
)


class ScriptedProvider:
    """Replays a fixed answer per task, keyed by a marker in the prompt.

    Responses are looked up by scanning the prompt for a registered key, which
    keeps the script readable and avoids threading task ids through the
    :class:`~drl_ai_core.providers.ModelProvider` interface just for testing.
    """

    def __init__(
        self,
        script: Mapping[str, str],
        *,
        provider_id: str = "scripted",
        model_family: str = "scripted-candidate",
        revision: str = "fixture-0.0.0",
        license_label: str = "Apache-2.0",
        default_response: str = "",
        latency_ms: float = 12.0,
        tool_calls: Mapping[str, tuple[dict[str, Any], ...]] | None = None,
        healthy: bool = True,
    ) -> None:
        self._script = dict(script)
        self._tool_calls = dict(tool_calls or {})
        self._identity = ModelIdentity(
            provider_id=provider_id,
            model_family=model_family,
            revision=revision,
            open_weight=True,
            output_mode=OutputMode.MOCK,
            license_label=license_label,
            runtime="scripted-fixture",
        )
        self.default_response = default_response
        self.latency_ms = latency_ms
        self.healthy = healthy

    @property
    def identity(self) -> ModelIdentity:
        return self._identity

    def health(self) -> bool:
        return self.healthy

    def _match(self, messages: Sequence[ChatMessage]) -> str | None:
        haystack = " ".join(m.content for m in messages).lower()
        for key in self._script:
            if key.lower() in haystack:
                return key
        return None

    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        tools: Sequence[dict[str, Any]] | None = None,
        constraints: CompletionConstraints,
    ) -> StructuredModelResponse:
        if not messages:
            raise ValueError("messages cannot be empty")
        if not self.healthy:
            raise ProviderUnavailableError(
                f"provider {self._identity.provider_id!r} is unavailable"
            )
        if constraints.require_open_weight and not self._identity.open_weight:
            raise ProviderUnavailableError("provider is not open-weight")

        key = self._match(messages)
        content = self._script.get(key, self.default_response) if key else self.default_response
        calls = self._tool_calls.get(key, ()) if key else ()
        return StructuredModelResponse(
            content=content,
            identity=self._identity,
            finish_reason="stop",
            latency_ms=self.latency_ms,
            usage={"prompt_tokens": 0, "completion_tokens": 0},
            tool_calls=tuple(calls),
        )
