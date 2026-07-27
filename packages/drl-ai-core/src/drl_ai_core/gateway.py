"""Model gateway with disclosed routing, timeout, and fallback policy."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .providers import (
    ChatMessage,
    ClosedWeightRejectedError,
    CompletionConstraints,
    ModelProvider,
    ProviderError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    StructuredModelResponse,
)


class ModelGateway:
    """Route completions through named providers with honest disclosure.

    Fallback is an explicit policy path. It never silently expands data rights
    or substitutes a closed-weight model when open weights are required.
    """

    def __init__(
        self,
        providers: Mapping[str, ModelProvider],
        *,
        primary: str,
        fallback: str | None = None,
    ) -> None:
        if not providers:
            raise ValueError("providers cannot be empty")
        if primary not in providers:
            raise ValueError(f"primary provider {primary!r} is not registered")
        if fallback is not None and fallback not in providers:
            raise ValueError(f"fallback provider {fallback!r} is not registered")
        self._providers = dict(providers)
        self.primary = primary
        self.fallback = fallback

    def provider(self, provider_id: str | None = None) -> ModelProvider:
        key = provider_id or self.primary
        try:
            return self._providers[key]
        except KeyError as exc:
            raise ProviderUnavailableError(f"provider {key!r} is not registered") from exc

    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        tools: Sequence[dict[str, Any]] | None = None,
        constraints: CompletionConstraints | None = None,
        route: str | None = None,
    ) -> StructuredModelResponse:
        constraints = constraints or CompletionConstraints()
        order = self._route_order(route)
        errors: list[str] = []

        for index, provider_id in enumerate(order):
            provider = self.provider(provider_id)
            identity = provider.identity
            if constraints.require_open_weight and not identity.open_weight:
                raise ClosedWeightRejectedError(
                    f"provider {provider_id!r} is closed-weight and open weights are required"
                )
            if (
                index > 0
                and not identity.open_weight
                and not constraints.allow_commercial_fallback
            ):
                raise ClosedWeightRejectedError(
                    f"commercial fallback {provider_id!r} is disabled for this request"
                )
            try:
                response = provider.complete(
                    messages,
                    tools=tools,
                    constraints=constraints,
                )
            except (ProviderTimeoutError, ProviderUnavailableError) as exc:
                errors.append(f"{provider_id}: {exc}")
                continue
            if index > 0:
                structured = dict(response.structured)
                structured["fallback_from"] = order[0]
                structured["fallback_errors"] = list(errors)
                return StructuredModelResponse(
                    content=response.content,
                    identity=response.identity,
                    finish_reason=response.finish_reason,
                    latency_ms=response.latency_ms,
                    usage=dict(response.usage),
                    tool_calls=response.tool_calls,
                    structured=structured,
                )
            return response

        detail = "; ".join(errors) if errors else "no provider available"
        raise ProviderError(f"all providers failed: {detail}")

    def _route_order(self, route: str | None) -> list[str]:
        if route is not None:
            order = [route]
            if self.fallback and self.fallback != route:
                order.append(self.fallback)
            return order
        order = [self.primary]
        if self.fallback and self.fallback != self.primary:
            order.append(self.fallback)
        return order
