"""Dependency composition for the local open DRL runtime."""

from __future__ import annotations

from atlas_service import AtlasService
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


def build_local_runtime() -> AtticusOrchestrator:
    """Build a zero-network runtime using synthetic, inspectable fixtures."""

    registry = ToolRegistry()
    register_foundation_tools(
        registry,
        atlas=AtlasService(),
        fedlens=FedLensService(),
        balancelab=ScenarioEngine(),
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
