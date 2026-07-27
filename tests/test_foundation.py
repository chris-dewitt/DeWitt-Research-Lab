from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_deep_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_foundation.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_requirement_and_work_package_scale() -> None:
    requirements = yaml.safe_load((ROOT / "requirements/requirements.yaml").read_text())
    work_packages = yaml.safe_load((ROOT / "requirements/work-packages.yaml").read_text())
    assert len(requirements["requirements"]) >= 100
    assert len(work_packages["work_packages"]) >= 95


def test_contract_examples_are_present() -> None:
    schemas = sorted((ROOT / "schemas").glob("*.schema.json"))
    examples = sorted((ROOT / "schemas/examples").glob("*.json"))
    assert len(schemas) == len(examples) >= 20
    for path in schemas + examples:
        json.loads(path.read_text(encoding="utf-8"))


def test_agent_missions_are_complete_set() -> None:
    missions = sorted((ROOT / "agents").glob("[0-9][0-9]_*.md"))
    assert [path.name[:2] for path in missions] == [f"{i:02d}" for i in range(16)]


def test_open_identity_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_open_identity.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_open_identity_contracts_are_present() -> None:
    reqs = yaml.safe_load((ROOT / "requirements/requirements.yaml").read_text())["requirements"]
    assert len([r for r in reqs if r["id"].startswith("DRL-OSS-")]) >= 26
    for name in ("open-artifact-release", "open-exception", "upstream-dependency"):
        assert (ROOT / "schemas" / f"{name}.schema.json").is_file()
        assert (ROOT / "schemas" / "examples" / f"{name}.json").is_file()
