"""Adapters that expose specialist domain logic through bounded tools."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Any

from atlas_service import AtlasService
from balancelab_ai import (
    SCENARIO_CATALOG,
    ScenarioEngine,
    project_named_scenario,
    sample_regional_bank,
)
from drl_protocol import EvidenceItem, RiskTier, ToolDefinition
from fedlens_service import FedLensService

from .registry import ToolOutput, ToolRegistry


def _parse_date(value: Any) -> date:
    if not isinstance(value, str):
        raise ValueError("as_of must be an ISO date string")
    return date.fromisoformat(value)


def _catalog_scenario_name(raw: str) -> str:
    """Map planner aliases onto the BalanceLab scenario catalog."""

    name = raw.strip()
    if name in SCENARIO_CATALOG:
        return name
    alias = name.removeprefix("synthetic-")
    if alias in SCENARIO_CATALOG:
        return alias
    raise KeyError(f"unknown scenario {raw!r}")


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
                    "DeWitt Research Workshop",
                    "Laboratory mission",
                    "2026-07-27",
                    "Intelligence for Good. Intelligence for All.",
                    "https://www.dewitt-labs.com",
                    {"topic": str(arguments.get("topic", ""))},
                )
            ],
            message=(
                "DeWitt Research Workshop is an independent, one-person open applied-AI "
                "research initiative led by Christopher Noxon DeWitt."
            ),
        ),
    )

    def atlas_handler(arguments: dict[str, Any]) -> ToolOutput:
        as_of = _parse_date(arguments["as_of"])
        items = atlas.research_snapshot(as_of=as_of)
        changes = atlas.series_changes(as_of=as_of)
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
                    "fixture": item.citation.startswith("fixture://"),
                },
            )
            for item in items
        ]
        message = f"Atlas returned {len(items)} point-in-time observations."
        if changes:
            message = f"{message} {len(changes)} series changed versus the prior print."
        return ToolOutput(
            evidence=evidence,
            artifacts={
                "atlas_snapshot": [asdict(item) for item in items],
                "series_changes": changes,
            },
            message=message,
        )

    registry.register(
        ToolDefinition(
            "atlas.research_snapshot",
            "Retrieve point-in-time macro and market evidence",
            RiskTier.READ_COMPUTE,
            True,
        ),
        atlas_handler,
    )

    def fedlens_handler(arguments: dict[str, Any]) -> ToolOutput:
        as_of = _parse_date(arguments["as_of"])
        document = fedlens.latest(as_of=as_of)
        cited = fedlens.compare_latest_cited(as_of=as_of)
        comparison = cited.comparison
        return ToolOutput(
            evidence=[
                EvidenceItem(
                    f"fedlens-{document.document_id}",
                    (
                        "DRL synthetic Federal Reserve fixture"
                        if document.citation.startswith("fixture://")
                        else "Federal Reserve monetary-policy press"
                    ),
                    document.title,
                    document.published_date.isoformat(),
                    document.text,
                    document.citation,
                    {
                        "fixture": document.citation.startswith("fixture://"),
                        "comparison": asdict(comparison),
                        "added_passage_citations": [p.citation for p in cited.added_passages],
                        "removed_passage_citations": [p.citation for p in cited.removed_passages],
                    },
                )
            ],
            artifacts={
                "fed_language_comparison": asdict(comparison),
                "fed_cited_comparison": {
                    "added_passages": [asdict(item) for item in cited.added_passages],
                    "removed_passages": [asdict(item) for item in cited.removed_passages],
                },
            },
            message=comparison.interpretation,
        )

    registry.register(
        ToolDefinition(
            "fedlens.compare_latest",
            "Compare the two latest eligible Fed communications",
            RiskTier.READ_COMPUTE,
            True,
        ),
        fedlens_handler,
    )

    def balancelab_handler(arguments: dict[str, Any]) -> ToolOutput:
        scenario_name = _catalog_scenario_name(str(arguments["name"]))
        bank = sample_regional_bank()
        artifact = project_named_scenario(bank, scenario_name, engine=balancelab)
        result = artifact.result
        content = (
            f"Synthetic annual NII change: ${result.annual_nii_change} million; "
            f"curve slope change: {result.curve_slope_change_bps} bps."
        )
        return ToolOutput(
            evidence=[
                EvidenceItem(
                    f"balancelab-{scenario_name}",
                    "BalanceLab deterministic scenario engine",
                    "Synthetic regional-bank rate scenario",
                    "2026-07-27",
                    content,
                    f"calculation://balancelab/{artifact.artifact_id}",
                    {
                        "fixture": True,
                        "lineage": list(result.calculation_lineage),
                        "artifact_digest": artifact.digest,
                    },
                )
            ],
            artifacts={
                "balance_sheet": asdict(bank.balance_sheet),
                "scenario_result": asdict(result),
                "calculation_artifact": {
                    "artifact_id": artifact.artifact_id,
                    "bank_id": artifact.bank_id,
                    "scenario_name": artifact.scenario_name,
                    "digest": artifact.digest,
                    "result": asdict(result),
                },
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
