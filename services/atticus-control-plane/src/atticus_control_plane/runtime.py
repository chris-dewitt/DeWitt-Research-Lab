"""Dependency composition for the local open DRL runtime."""

from __future__ import annotations

import os
from pathlib import Path
from tempfile import gettempdir

from atlas_service import AtlasService, FileObservationCache, PublicFixtureAdapter
from balancelab_ai import ScenarioEngine
from drl_ai_core import HttpOpenAICompatibleProvider, ModelGateway
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


def build_http_model_gateway(
    *,
    model: str,
    base_url: str | None = None,
    license_label: str = "unreviewed",
    quantization: str | None = None,
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
    )
    return ModelGateway({provider.identity.provider_id: provider},
                        primary=provider.identity.provider_id)


def build_model_backed_runtime(
    *,
    model: str,
    base_url: str | None = None,
    license_label: str = "unreviewed",
) -> AtticusOrchestrator:
    """Build the local runtime with an open-weight model doing the planning.

    Everything downstream of the planner is unchanged: the same specialists, the
    same policy engine, the same approvals and evaluation. Only the source of the
    plan differs, and a model failure falls back to the deterministic planner.
    """
    orchestrator = build_local_runtime()
    gateway = build_http_model_gateway(
        model=model, base_url=base_url, license_label=license_label
    )
    orchestrator.planner = ModelPlanner(gateway, orchestrator.registry.catalog())
    return orchestrator


def build_runtime_from_env() -> AtticusOrchestrator:
    """Build the runtime, using a model planner when ATTICUS_MODEL is set.

    Unset means the deterministic fixture path, which is the default everywhere
    including CI. Setting the variable is the single switch that puts a model
    behind Atticus.
    """
    model = os.environ.get("ATTICUS_MODEL", "").strip()
    if not model:
        return build_local_runtime()
    return build_model_backed_runtime(
        model=model,
        base_url=os.environ.get("ATTICUS_MODEL_BASE_URL") or None,
        license_label=os.environ.get("ATTICUS_MODEL_LICENSE", "unreviewed"),
    )
