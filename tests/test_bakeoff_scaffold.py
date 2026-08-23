"""Tests for Atticus bake-off scaffolding (DRL-012)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from drl_ai_core import load_bakeoff_register, run_bakeoff_scaffold

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "models" / "bakeoff" / "candidates.yaml"


def test_local_edge_models_are_registered_as_served() -> None:
    """Qwen3-1.7B and SmolLM3-3B are workstation-served, not a DIR-004 winner."""
    register = load_bakeoff_register(REGISTER)
    by_id = {row["id"]: row for row in register["candidates"]}
    for candidate_id, expected_model in (
        ("edge-qwen3-1.7b", "qwen3:1.7b"),
        ("edge-smollm3-3b", "hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M"),
    ):
        row = by_id[candidate_id]
        assert row["role"] == "edge"
        assert row["open_weight"] is True
        assert row["license_status"] != "cleared"
        serving = row["serving"]
        assert serving["runtime"] == "ollama"
        assert serving["model"] == expected_model
    assert register["selection_status"] == "not_selected"


def test_bakeoff_register_covers_core_and_edge() -> None:
    register = load_bakeoff_register(REGISTER)
    roles = {row["role"] for row in register["candidates"]}
    assert roles == {"core", "edge"}
    assert register["selection_status"] == "not_selected"
    assert register["director_gate"] == "DIR-004"
    for row in register["candidates"]:
        assert row["open_weight"] is True
        assert row["license_label"]
        assert row["hardware_class"]
        assert row["cost_tier"]
        assert row["limitations"]


def test_bakeoff_scaffold_report_has_required_fields() -> None:
    report = run_bakeoff_scaffold(REGISTER)
    assert report["selection_status"] == "not_selected"
    assert report["family_coverage"]["coordinated_family"] is True
    assert report["family_coverage"]["core_count"] >= 1
    assert report["family_coverage"]["edge_count"] >= 1
    for row in report["candidates"]:
        assert "license" in row
        assert "hardware" in row
        assert "cost_tier" in row
        assert "latency_proxy" in row
        assert "quality_proxy" in row
        assert "limitations" in row
        assert 0.0 <= row["metrics"]["aggregate_proxy"] <= 1.0
    assert any(
        "DIR-004" in item or "not selected" in item.lower() for item in report["limitations"]
    )
    assert report["configuration_digest"].startswith("sha256:")


def test_bakeoff_scaffold_rejects_declared_winner(tmp_path: Path) -> None:
    data = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    data["selection_status"] = "selected"
    bad = tmp_path / "bad.yaml"
    bad.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(ValueError, match="selected winner"):
        load_bakeoff_register(bad)
