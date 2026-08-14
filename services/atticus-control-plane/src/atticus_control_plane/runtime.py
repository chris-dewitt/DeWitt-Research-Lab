"""Dependency composition for the local open DRL runtime."""

from __future__ import annotations

import os
from pathlib import Path
from tempfile import gettempdir

from atlas_service import AtlasService, FileObservationCache, PublicFixtureAdapter
from balancelab_ai import ScenarioEngine
from drl_ai_core import HttpOpenAICompatibleProvider, ModelGateway
from drl_ai_core.http_provider import DEFAULT_STALL_TIMEOUT_SECONDS, THINKING_OFF_HINTS
from drl_ai_core.providers import CompletionConstraints
from evalforge_service import EvalForge
from fedlens_service import FedLensService

from .approvals import ApprovalService
from .model_gateway import build_local_model_gateway
from .model_planner import ModelPlanner
from .orchestrator import AtticusOrchestrator
from .policy import PolicyEngine
from .registry import ToolRegistry
from .tools import register_foundation_tools


def build_m3_specialists() -> tuple[AtlasService, FedLensService, ScenarioEngine]:
    """Compose M3 fixture specialists (Atlas adapter, FedLens corpus, BalanceLab)."""

    cache_root = Path(gettempdir()) / "drl-atlas-public-fixture-cache"
    atlas = AtlasService.from_public_adapter(
        PublicFixtureAdapter(cache=FileObservationCache(cache_root))
    )
    fedlens = FedLensService.from_bounded_corpus()
    return atlas, fedlens, ScenarioEngine()


def build_local_runtime() -> AtticusOrchestrator:
    """Build a zero-network runtime using synthetic, inspectable fixtures."""

    atlas, fedlens, balancelab = build_m3_specialists()
    registry = ToolRegistry()
    register_foundation_tools(
        registry,
        atlas=atlas,
        fedlens=fedlens,
        balancelab=balancelab,
    )
    return AtticusOrchestrator(
        registry=registry,
        policy=PolicyEngine(),
        approvals=ApprovalService(),
        evaluator=EvalForge(),
    )


def build_local_open_weight_gateway() -> ModelGateway:
    """Build the unpaid open-weight model gateway used by local demos."""

    return build_local_model_gateway()


#: Default local runtime endpoint. Ollama, vLLM, LM Studio, and llama-server all
#: expose this shape, so switching runtime is configuration, not code.
DEFAULT_MODEL_BASE_URL = "http://localhost:11434/v1"

#: Runaway ceiling on a single planning call, in seconds.
#:
#: This is not an estimate of how long the model *ought* to take. Because the
#: provider streams, a stalled endpoint is caught by the stall timeout in a
#: couple of minutes regardless of this number, so the total budget only has to
#: be large enough that a slow-but-working local model is never killed
#: mid-generation. Fifteen minutes clears CPU-bound generation on a 26B model.
DEFAULT_MODEL_TIMEOUT_SECONDS = 900.0

#: Seconds of silence from the endpoint before the call is declared dead.
DEFAULT_MODEL_STALL_TIMEOUT_SECONDS = DEFAULT_STALL_TIMEOUT_SECONDS

#: Env values read as true for boolean switches.
_TRUTHY = {"1", "true", "yes", "on"}


def _flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in _TRUTHY


def _positive_float(name: str) -> float | None:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    return value if value > 0 else None


def build_http_model_gateway(
    *,
    model: str,
    base_url: str | None = None,
    license_label: str = "unreviewed",
    quantization: str | None = None,
    stream: bool = True,
    stall_timeout: float | None = None,
    disable_thinking: bool = False,
) -> ModelGateway:
    """Build a gateway backed by a locally hosted open-weight model.

    ``license_label`` is recorded from the model register rather than probed; an
    endpoint cannot attest to the license of the weights it loaded.
    """
    provider = HttpOpenAICompatibleProvider(
        model=model,
        base_url=base_url or DEFAULT_MODEL_BASE_URL,
        provider_id=f"local::{model}",
        model_family=model.split(":", 1)[0],
        license_label=license_label,
        quantization=quantization,
        stream=stream,
        stall_timeout=stall_timeout or DEFAULT_MODEL_STALL_TIMEOUT_SECONDS,
        extra_payload=dict(THINKING_OFF_HINTS) if disable_thinking else None,
    )
    return ModelGateway({provider.identity.provider_id: provider},
                        primary=provider.identity.provider_id)


def build_model_backed_runtime(
    *,
    model: str,
    base_url: str | None = None,
    license_label: str = "unreviewed",
    timeout_seconds: float | None = None,
    stall_timeout_seconds: float | None = None,
    max_output_tokens: int = 2048,
    stream: bool = True,
    disable_thinking: bool = False,
) -> AtticusOrchestrator:
    """Build the local runtime with an open-weight model doing the planning.

    Everything downstream of the planner is unchanged: the same specialists, the
    same policy engine, the same approvals and evaluation. Only the source of the
    plan differs, and a model failure falls back to the deterministic planner.
    """
    orchestrator = build_local_runtime()
    gateway = build_http_model_gateway(
        model=model,
        base_url=base_url,
        license_label=license_label,
        stream=stream,
        stall_timeout=stall_timeout_seconds,
        disable_thinking=disable_thinking,
    )
    constraints = CompletionConstraints(
        temperature=0.0,
        max_output_tokens=max_output_tokens,
        require_open_weight=True,
        timeout_seconds=timeout_seconds or DEFAULT_MODEL_TIMEOUT_SECONDS,
    )
    orchestrator.planner = ModelPlanner(
        gateway, orchestrator.registry.catalog(), constraints=constraints
    )
    return orchestrator


def build_runtime_from_env() -> AtticusOrchestrator:
    """Build the runtime, using a model planner when ATTICUS_MODEL is set.

    Unset means the deterministic fixture path, which is the default everywhere
    including CI. Setting the variable is the single switch that puts a model
    behind Atticus. The rest are escape hatches for a runtime that behaves
    differently from the defaults:

    ``ATTICUS_MODEL_BASE_URL``      non-default endpoint (vLLM, LM Studio, ...)
    ``ATTICUS_MODEL_LICENSE``       license recorded in the disclosure
    ``ATTICUS_MODEL_TIMEOUT``       total ceiling on one planning call
    ``ATTICUS_MODEL_STALL_TIMEOUT`` silence tolerated before declaring it dead
    ``ATTICUS_MODEL_MAX_TOKENS``    output budget for the plan
    ``ATTICUS_MODEL_NO_STREAM``     fall back to one blocking request
    ``ATTICUS_MODEL_NO_THINKING``   ask a reasoning model to answer directly
    """
    model = os.environ.get("ATTICUS_MODEL", "").strip()
    if not model:
        return build_local_runtime()
    max_tokens = _positive_float("ATTICUS_MODEL_MAX_TOKENS")
    return build_model_backed_runtime(
        model=model,
        base_url=os.environ.get("ATTICUS_MODEL_BASE_URL") or None,
        license_label=os.environ.get("ATTICUS_MODEL_LICENSE", "unreviewed"),
        timeout_seconds=_positive_float("ATTICUS_MODEL_TIMEOUT"),
        stall_timeout_seconds=_positive_float("ATTICUS_MODEL_STALL_TIMEOUT"),
        max_output_tokens=int(max_tokens) if max_tokens else 2048,
        stream=not _flag("ATTICUS_MODEL_NO_STREAM"),
        disable_thinking=_flag("ATTICUS_MODEL_NO_THINKING"),
    )
