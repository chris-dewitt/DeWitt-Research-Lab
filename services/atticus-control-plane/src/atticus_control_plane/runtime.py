"""Dependency composition for the local open DRL runtime."""

from __future__ import annotations

from pathlib import Path
from tempfile import gettempdir

from atlas_service import AtlasService, FileObservationCache, PublicFixtureAdapter
from balancelab_ai import ScenarioEngine
from drl_ai_core import ModelGateway
from evalforge_service import EvalForge
from fedlens_service import FedLensService

from .approvals import ApprovalService
from .model_gateway import build_local_model_gateway
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
