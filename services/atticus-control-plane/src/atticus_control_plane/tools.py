"""Adapters that expose specialist domain logic through bounded tools."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date
from decimal import Decimal
from typing import Any

from atlas_service import AtlasService
from balancelab_ai import BalanceSheet, RateScenario, ScenarioEngine
from drl_protocol import EvidenceItem, RiskTier, ToolDefinition
from fedlens_service import FedLensService

from .registry import ToolOutput, ToolRegistry


def _parse_date(value: Any) -> date:
    if not isinstance(value, str):
        raise ValueError("as_of must be an ISO date string")
    return date.fromisoformat(value)


def register_foundation_tools(
    registry: ToolRegistry,
    *,
    atlas: AtlasService,
    fedlens: FedLensService,
    balancelab: ScenarioEngine,
) -> None:
    """Register public-safe fixture tools for the integrated local demo."""

    registry.register(
        ToolDefinition(
            "laboratory.guide",
            "Explain the DRL mission and supported research systems",
            RiskTier.EXPLAIN,
            True,
        ),
        lambda arguments: ToolOutput(
            evidence=[
                EvidenceItem(
                    "drl-mission",
                    "DeWitt Research Laboratory",
                    "Laboratory mission",
                    "2026-07-27",
                    "AI for Good. AI for all. Intelligence of the people and for the people.",
                    "https://www.dwit-labs.com",
                    {"topic": str(arguments.get("topic", ""))},
                )
            ],
            message=(
                "DeWitt Research Laboratory is an independent, one-person open applied-AI "
                "research initiative led by DeWitt."
            ),
        ),
    )

    def atlas_handler(arguments: dict[str, Any]) -> ToolOutput:
        as_of = _parse_date(arguments["as_of"])
        items = atlas.research_snapshot(as_of=as_of)
        evidence = [
            EvidenceItem(
                f"atlas-{item.series_id}-{item.observation_date.isoformat()}",
                item.source,
                item.title,
                item.published_date.isoformat(),
                f"{item.value} {item.unit}",
                item.citation,
                {
                    "series_id": item.series_id,
                    "observation_date": item.observation_date.isoformat(),
                    "as_of": as_of.isoformat(),
                    "fixture": True,
                },
            )
            for item in items
        ]
        return ToolOutput(
            evidence=evidence,
            artifacts={"atlas_snapshot": [asdict(item) for item in items]},
            message=f"Atlas returned {len(items)} point-in-time observations.",
        )

    registry.register(
        ToolDefinition(
            "atlas.research_snapshot",
            "Retrieve point-in-time macro and market fixture evidence",
            RiskTier.READ_COMPUTE,
            True,
        ),
        atlas_handler,
    )

    def fedlens_handler(arguments: dict[str, Any]) -> ToolOutput:
        as_of = _parse_date(arguments["as_of"])
        document = fedlens.latest(as_of=as_of)
        comparison = fedlens.compare_latest(as_of=as_of)
        return ToolOutput(
            evidence=[
                EvidenceItem(
                    f"fedlens-{document.document_id}",
                    "DRL synthetic Federal Reserve fixture",
                    document.title,
                    document.published_date.isoformat(),
                    document.text,
                    document.citation,
                    {"fixture": True, "comparison": asdict(comparison)},
                )
            ],
            artifacts={"fed_language_comparison": asdict(comparison)},
            message=comparison.interpretation,
        )

    registry.register(
        ToolDefinition(
            "fedlens.compare_latest",
            "Compare the two latest eligible Fed communication fixtures",
            RiskTier.READ_COMPUTE,
            True,
        ),
        fedlens_handler,
    )

    def balancelab_handler(arguments: dict[str, Any]) -> ToolOutput:
        scenario = RateScenario(
            str(arguments["name"]),
            int(arguments["short_rate_bps"]),
            int(arguments["long_rate_bps"]),
        )
        sample_bank = BalanceSheet(
            earning_assets=Decimal("8500"),
            interest_bearing_deposits=Decimal("6200"),
            wholesale_funding=Decimal("900"),
        )
        result = balancelab.project(sample_bank, scenario)
        content = (
            f"Synthetic annual NII change: ${result.annual_nii_change} million; "
            f"curve slope change: {result.curve_slope_change_bps} bps."
        )
        return ToolOutput(
            evidence=[
                EvidenceItem(
                    f"balancelab-{scenario.name}",
                    "BalanceLab deterministic scenario engine",
                    "Synthetic regional-bank rate scenario",
                    "2026-07-27",
                    content,
                    "calculation://balancelab/synthetic-bear-steepener",
                    {
                        "fixture": True,
                        "lineage": list(result.calculation_lineage),
                    },
                )
            ],
            artifacts={
                "balance_sheet": asdict(sample_bank),
                "scenario_result": asdict(result),
            },
            message=content,
        )

    registry.register(
        ToolDefinition(
            "balancelab.run_scenario",
            "Run a deterministic scenario against a synthetic balance sheet",
            RiskTier.READ_COMPUTE,
            True,
        ),
        balancelab_handler,
    )
