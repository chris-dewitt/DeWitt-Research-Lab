"""Deterministic Atticus Core/Edge bake-off scaffolding (DRL-012).

Loads a versioned candidate register and fixture metrics, emits a report with
license/hardware/cost/latency/quality/limitation fields, and never declares a
selected base model. DIR-004 remains the Director evidence gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .security import canonical_digest

DEFAULT_REGISTER = Path(__file__).resolve().parents[4] / "models" / "bakeoff" / "candidates.yaml"


@dataclass(frozen=True, slots=True)
class ServingSpec:
    """Where a candidate can actually be reached, when one has been stood up.

    Its presence is the whole switch for a live run. A candidate without a
    ``serving`` block is skipped rather than scored zero — nobody has served it,
    which is not the same as it having failed.
    """

    runtime: str
    model: str
    base_url: str | None = None
    quantization: str | None = None
    system_prefix: str | None = None
    """Text the runtime needs in the system message before it will answer.

    Hybrid reasoning models decide whether to emit a thinking block, and left
    unsuppressed both edge candidates spend the entire output budget inside it
    and return empty content — so a live run measures nothing.

    ``THINKING_OFF_HINTS`` already asks for this through the request body, and
    its own docstring is careful to call that best-effort. Measured against
    ollama's OpenAI-compatible shim on 2026-08-25, it is: both ``think: false``
    and ``chat_template_kwargs.enable_thinking`` are accepted without error and
    have no effect on ``hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M``, which still
    returned 96 thinking tokens and empty content. The control token in the
    system message did work. The two mechanisms are complementary rather than
    redundant: the payload hints reach servers that implement them, and this
    reaches models whose chat template only reads the conversation.

    It belongs on the serving block because it is a property of how this
    candidate is served, not of the task being asked.
    """


@dataclass(frozen=True, slots=True)
class BakeoffCandidate:
    id: str
    role: str
    family: str
    license_label: str
    license_status: str
    open_weight: bool
    hardware_class: str
    estimated_vram_gb: float
    cost_tier: str
    source_url: str
    limitations: tuple[str, ...]
    revision_label: str
    serving: ServingSpec | None = None


def parse_serving(raw: Any) -> ServingSpec | None:
    """Read a candidate's ``serving`` block, if it has one."""
    if not isinstance(raw, dict):
        return None
    runtime = str(raw.get("runtime", "")).strip()
    model = str(raw.get("model", "")).strip()
    if not runtime or not model:
        raise ValueError("serving block requires both 'runtime' and 'model'")
    base_url = raw.get("base_url")
    quantization = raw.get("quantization")
    system_prefix = raw.get("system_prefix")
    return ServingSpec(
        runtime=runtime,
        model=model,
        base_url=str(base_url) if base_url else None,
        quantization=str(quantization) if quantization else None,
        system_prefix=str(system_prefix) if system_prefix else None,
    )


def load_bakeoff_register(path: Path | None = None) -> dict[str, Any]:
    register_path = path or DEFAULT_REGISTER
    raw = yaml.safe_load(register_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("bake-off register must be a mapping")
    if raw.get("selection_status") == "selected":
        raise ValueError("scaffold register must not declare a selected winner")
    return raw


def _candidate(row: dict[str, Any]) -> BakeoffCandidate:
    return BakeoffCandidate(
        id=str(row["id"]),
        role=str(row["role"]),
        family=str(row["family"]),
        license_label=str(row["license_label"]),
        license_status=str(row["license_status"]),
        open_weight=bool(row["open_weight"]),
        hardware_class=str(row["hardware_class"]),
        estimated_vram_gb=float(row["estimated_vram_gb"]),
        cost_tier=str(row["cost_tier"]),
        source_url=str(row["source_url"]),
        limitations=tuple(str(item) for item in row.get("limitations", [])),
        revision_label=str(row.get("revision_label", "unpinned")),
        serving=parse_serving(row.get("serving")),
    )


def score_candidate(metrics: dict[str, float]) -> dict[str, float]:
    keys = (
        "license_clarity",
        "runtime_fit",
        "structured_output",
        "tool_use",
        "latency_proxy",
        "cost_efficiency",
        "quality_proxy",
    )
    missing = [key for key in keys if key not in metrics]
    if missing:
        raise ValueError(f"fixture metrics missing keys: {missing}")
    values = [float(metrics[key]) for key in keys]
    if any(value < 0 or value > 1 for value in values):
        raise ValueError("fixture metrics must be in [0, 1]")
    # Equal-weight scaffold aggregate; never used as a selection decision.
    aggregate = round(sum(values) / len(values), 3)
    return {**{key: float(metrics[key]) for key in keys}, "aggregate_proxy": aggregate}


def run_bakeoff_scaffold(path: Path | None = None) -> dict[str, Any]:
    """Return a reproducible scaffold report without selecting a model."""

    register = load_bakeoff_register(path)
    fixture_metrics = dict(register.get("fixture_metrics") or {})
    candidates = [_candidate(row) for row in register.get("candidates", [])]
    if not candidates:
        raise ValueError("bake-off register requires at least one candidate")

    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        if not candidate.open_weight:
            raise ValueError(f"closed-weight candidate forbidden in scaffold: {candidate.id}")
        metrics = score_candidate(dict(fixture_metrics[candidate.id]))
        rows.append(
            {
                "id": candidate.id,
                "role": candidate.role,
                "family": candidate.family,
                "revision_label": candidate.revision_label,
                "license": {
                    "label": candidate.license_label,
                    "status": candidate.license_status,
                },
                "hardware": {
                    "class": candidate.hardware_class,
                    "estimated_vram_gb": candidate.estimated_vram_gb,
                },
                "cost_tier": candidate.cost_tier,
                "latency_proxy": metrics["latency_proxy"],
                "quality_proxy": metrics["quality_proxy"],
                "metrics": metrics,
                "limitations": list(candidate.limitations),
                "source_url": candidate.source_url,
            }
        )

    core = [row for row in rows if row["role"] == "core"]
    edge = [row for row in rows if row["role"] == "edge"]
    if not core or not edge:
        raise ValueError("scaffold requires both core and edge candidates")

    payload = {
        "suite_id": register.get("suite_id", "atticus.bakeoff.scaffold"),
        "suite_version": register.get("suite_version", "1.0.0"),
        "as_of": register.get("as_of"),
        "selection_status": "not_selected",
        "director_gate": register.get("director_gate", "DIR-004"),
        "maturity": "prototype-scaffold",
        "runtimes": list(register.get("runtimes") or []),
        "candidates": rows,
        "family_coverage": {
            "core_count": len(core),
            "edge_count": len(edge),
            "coordinated_family": True,
        },
        "limitations": list(register.get("notes") or [])
        + [
            "Fixture metrics are synthetic and must not be cited as measured bake-off results.",
            "No base model is selected; DIR-004 remains open.",
        ],
    }
    payload["configuration_digest"] = f"sha256:{canonical_digest(payload)}"
    return payload
