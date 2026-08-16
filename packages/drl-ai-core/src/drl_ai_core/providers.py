"""Typed open-weight model provider contracts.

These abstractions are provider-neutral. They disclose model identity and
output mode, enforce open-weight policy at the call boundary, and never treat
model text as authorization.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol


class OutputMode(StrEnum):
    """Honest label for how a completion was produced."""

    LIVE = "live"
    MOCK = "mock"
    REPLAY = "replay"
    CACHED = "cached"


@dataclass(frozen=True, slots=True)
class ModelIdentity:
    """Exact, disclosable model path used for a completion."""

    provider_id: str
    model_family: str
    revision: str
    open_weight: bool
    output_mode: OutputMode
    license_label: str
    quantization: str | None = None
    runtime: str | None = None

    def disclosure(self) -> dict[str, Any]:
        """Return a trace/UI-safe identity payload."""

        return {
            "provider_id": self.provider_id,
            "model_family": self.model_family,
            "revision": self.revision,
            "open_weight": self.open_weight,
            "output_mode": self.output_mode.value,
            "license_label": self.license_label,
            "quantization": self.quantization,
            "runtime": self.runtime,
        }


@dataclass(frozen=True, slots=True)
class ChatMessage:
    """One chat turn. Content is treated as data, never as policy."""

    role: str
    content: str


@dataclass(frozen=True, slots=True)
class CompletionConstraints:
    """Control-plane budgets enforced around provider calls."""

    timeout_seconds: float = 30.0
    max_output_tokens: int = 1024
    temperature: float = 0.0
    require_open_weight: bool = True
    allow_commercial_fallback: bool = False
    #: Stop reading as soon as one complete JSON value has been generated.
    #:
    #: ``max_output_tokens`` is a ceiling, not a target, and a local model asked
    #: for JSON routinely emits the object and then keeps going — restating the
    #: plan in prose, adding a second example, apologising. Every token after the
    #: closing brace is generated at full cost and then discarded by the parser.
    #: With this set, a provider that streams may close the connection at that
    #: brace; the runtime abandons the rest of the generation.
    #:
    #: Only set it where the response *is* a JSON document. On a completion
    #: whose text merely contains JSON, this truncates the answer. Providers that
    #: cannot stream ignore it — the tokens are already spent by the time the
    #: body arrives.
    stop_after_json: bool = False

    def __post_init__(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
        if self.temperature < 0:
            raise ValueError("temperature cannot be negative")


@dataclass(frozen=True, slots=True)
class StructuredModelResponse:
    """Provider result with mandatory identity and usage disclosure."""

    content: str
    identity: ModelIdentity
    finish_reason: str
    latency_ms: float
    usage: dict[str, int] = field(default_factory=dict)
    tool_calls: tuple[dict[str, Any], ...] = ()
    structured: dict[str, Any] = field(default_factory=dict)
    #: How the completion was carried, not what it said: whether it streamed,
    #: how many chunks arrived, time to first token. Diagnosing a slow local
    #: endpoint needs this, and total latency alone cannot supply it — a long
    #: wait before the first token and a long steady generation are different
    #: faults with different fixes.
    transport: dict[str, Any] = field(default_factory=dict)

    def disclosure(self) -> dict[str, Any]:
        payload = self.identity.disclosure()
        payload.update(
            {
                "finish_reason": self.finish_reason,
                "latency_ms": self.latency_ms,
                "usage": dict(self.usage),
            }
        )
        if self.transport:
            payload["transport"] = dict(self.transport)
        return payload


class ProviderError(RuntimeError):
    """Base error for model provider failures."""


class ProviderTimeoutError(ProviderError):
    """Raised when a provider exceeds its timeout budget."""


class ProviderUnavailableError(ProviderError):
    """Raised when a provider is unhealthy or refuses the request."""


class ClosedWeightRejectedError(ProviderError):
    """Raised when a closed-weight route is requested on an open-weight path."""


class ModelProvider(Protocol):
    """Structural interface for live and mock open-weight endpoints."""

    @property
    def identity(self) -> ModelIdentity:
        """Static identity advertised by this provider instance."""

    def health(self) -> bool:
        """Return True when the provider can accept work."""

    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        tools: Sequence[dict[str, Any]] | None = None,
        constraints: CompletionConstraints,
    ) -> StructuredModelResponse:
        """Produce a completion under the supplied constraints."""
