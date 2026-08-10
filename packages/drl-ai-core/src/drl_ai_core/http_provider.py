"""OpenAI-compatible HTTP provider for locally hosted open-weight models.

One adapter covers every local runtime worth using — Ollama, vLLM, LM Studio, and
``llama-server`` all expose the same ``/v1/chat/completions`` shape — so the
workshop can change runtime without changing code.

Two behaviours here are deliberate rather than incidental:

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
from collections.abc import Sequence
from http.client import HTTPException
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

__all__ = ["HttpOpenAICompatibleProvider"]

#: Fenced reasoning blocks emitted inline by some reasoning models.
_THINK_BLOCK = re.compile(r"<think>.*?</think>\s*", re.DOTALL | re.IGNORECASE)

#: Keys under which runtimes return separate reasoning content.
_REASONING_KEYS = ("reasoning", "reasoning_content", "thinking")


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
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.connect_timeout = connect_timeout
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

    def _post(self, path: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if not url.startswith(("http://localhost", "http://127.0.0.1", "https://")):
            raise ProviderUnavailableError(
                f"refusing non-local plaintext endpoint: {url}"
            )
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = urllib.request.Request(  # noqa: S310 - scheme checked above
            url, data=json.dumps(payload).encode(), headers=headers
        )
        try:
            # The scheme is validated above: only loopback HTTP or HTTPS reaches
            # this call, so file:// and custom schemes cannot.
            with urllib.request.urlopen(  # noqa: S310  # nosec B310
                request, timeout=timeout
            ) as response:
                body = response.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:300]
            raise ProviderUnavailableError(
                f"endpoint returned HTTP {exc.code}: {detail}"
            ) from exc
        except TimeoutError as exc:
            raise ProviderTimeoutError(f"endpoint timed out after {timeout:.1f}s") from exc
        except (urllib.error.URLError, OSError, HTTPException) as exc:
            reason = getattr(exc, "reason", exc)
            if isinstance(reason, TimeoutError):
                raise ProviderTimeoutError(
                    f"endpoint timed out after {timeout:.1f}s"
                ) from exc
            raise ProviderUnavailableError(f"cannot reach {url}: {reason}") from exc

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ProviderUnavailableError(
                f"endpoint returned non-JSON: {body[:200]}"
            ) from exc
        if not isinstance(parsed, dict):
            raise ProviderUnavailableError("endpoint returned a non-object response")
        return parsed

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

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": constraints.temperature,
            "max_tokens": constraints.max_output_tokens,
            "stream": False,
        }
        if tools:
            payload["tools"] = list(tools)

        started = time.perf_counter()
        body = self._post(
            "/chat/completions", payload, timeout=constraints.timeout_seconds
        )
        latency_ms = (time.perf_counter() - started) * 1000

        choices = body.get("choices") or []
        if not choices or not isinstance(choices[0], dict):
            raise ProviderUnavailableError("endpoint returned no choices")
        choice = choices[0]
        message = choice.get("message") or {}

        raw = str(message.get("content") or "")
        content = strip_reasoning(raw)
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

        usage_raw = body.get("usage") or {}
        usage = {
            k: int(v)
            for k, v in usage_raw.items()
            if isinstance(v, int | float) and not isinstance(v, bool)
        }

        return StructuredModelResponse(
            content=content,
            identity=self._identity,
            finish_reason=str(choice.get("finish_reason") or "stop"),
            latency_ms=latency_ms,
            usage=usage,
            tool_calls=tuple(tool_calls),
        )
