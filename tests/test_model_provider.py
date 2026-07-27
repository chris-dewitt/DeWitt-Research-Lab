"""Tests for the typed open-weight provider interface and model gateway."""

from __future__ import annotations

import pytest
from atticus_control_plane import build_local_model_gateway, build_local_runtime
from drl_ai_core import (
    ChatMessage,
    ClosedWeightRejectedError,
    CompletionConstraints,
    MockOpenWeightProvider,
    ModelGateway,
    ModelIdentity,
    OutputMode,
    ProviderTimeoutError,
    ProviderUnavailableError,
)
from drl_protocol import RunState, TaskRequest


def test_mock_provider_discloses_open_weight_identity() -> None:
    provider = MockOpenWeightProvider()
    response = provider.complete(
        [ChatMessage("user", "Explain Atticus")],
        constraints=CompletionConstraints(),
    )

    assert response.identity.open_weight is True
    assert response.identity.output_mode is OutputMode.MOCK
    assert response.disclosure()["provider_id"] == "mock-open-weight"
    assert "MOCK OPEN-WEIGHT RESPONSE" in response.content
    assert response.usage["completion_tokens"] > 0


def test_mock_provider_timeout_is_enforced() -> None:
    provider = MockOpenWeightProvider(latency_seconds=0.05)
    with pytest.raises(ProviderTimeoutError, match="timeout"):
        provider.complete(
            [ChatMessage("user", "slow")],
            constraints=CompletionConstraints(timeout_seconds=0.01),
        )


def test_mock_provider_unavailable_error() -> None:
    provider = MockOpenWeightProvider(fail_closed=True)
    assert provider.health() is False
    with pytest.raises(ProviderUnavailableError):
        provider.complete(
            [ChatMessage("user", "hello")],
            constraints=CompletionConstraints(),
        )


def test_gateway_falls_back_and_discloses_fallback() -> None:
    primary = MockOpenWeightProvider(
        provider_id="primary",
        fail_closed=True,
    )
    fallback = MockOpenWeightProvider(
        provider_id="fallback",
        model_family="atticus-edge",
        revision="edge-fixture",
    )
    gateway = ModelGateway(
        {"primary": primary, "fallback": fallback},
        primary="primary",
        fallback="fallback",
    )

    response = gateway.complete([ChatMessage("user", "Need a plan")])

    assert response.identity.provider_id == "fallback"
    assert response.structured["fallback_from"] == "primary"
    assert response.structured["fallback_errors"]


def test_gateway_rejects_closed_weight_when_open_required() -> None:
    class Closed:
        @property
        def identity(self) -> ModelIdentity:
            return ModelIdentity(
                provider_id="closed",
                model_family="secret-saas",
                revision="1",
                open_weight=False,
                output_mode=OutputMode.LIVE,
                license_label="proprietary",
            )

        def health(self) -> bool:
            return True

        def complete(
            self,
            messages: list[ChatMessage],
            *,
            tools: list[dict[str, object]] | None = None,
            constraints: CompletionConstraints | None = None,
        ) -> object:
            raise AssertionError("must not be called")

    gateway = ModelGateway({"closed": Closed()}, primary="closed")
    with pytest.raises(ClosedWeightRejectedError):
        gateway.complete(
            [ChatMessage("user", "secret")],
            constraints=CompletionConstraints(require_open_weight=True),
        )


def test_gateway_rejects_commercial_fallback_by_default() -> None:
    primary = MockOpenWeightProvider(provider_id="primary", fail_closed=True)
    commercial = build_local_model_gateway(include_commercial_stub=True).provider(
        "commercial-stub"
    )
    gateway = ModelGateway(
        {"primary": primary, "commercial-stub": commercial},
        primary="primary",
        fallback="commercial-stub",
    )
    with pytest.raises(ClosedWeightRejectedError, match="open weights are required"):
        gateway.complete(
            [ChatMessage("user", "fallback?")],
            constraints=CompletionConstraints(
                require_open_weight=True,
                allow_commercial_fallback=False,
            ),
        )


def test_local_atticus_gateway_keeps_demo_unpaid() -> None:
    gateway = build_local_model_gateway()
    response = gateway.complete(
        [ChatMessage("user", "Use inflation evidence")],
        tools=[{"name": "atlas.research_snapshot"}],
        constraints=CompletionConstraints(require_open_weight=True),
    )
    assert response.identity.open_weight is True
    assert response.identity.output_mode is OutputMode.MOCK
    assert "paid" not in response.content.lower() or "does not call a paid" in response.content


def test_fixture_runtime_still_completes_without_paid_api() -> None:
    result = build_local_runtime().run(
        TaskRequest(
            "provider-demo",
            "Use inflation and Federal Reserve evidence to run a bear-steepener bank scenario",
            public_session=True,
            as_of="2026-07-24",
        )
    )
    assert result.state is RunState.COMPLETED
    assert result.evaluation["passed"] is True


def test_empty_messages_rejected() -> None:
    with pytest.raises(ValueError, match="messages"):
        MockOpenWeightProvider().complete([], constraints=CompletionConstraints())


def test_invalid_constraints_rejected() -> None:
    with pytest.raises(ValueError):
        CompletionConstraints(timeout_seconds=0)
