"""Tests for the local Ollama catalogue checker.

The checker exists because `ollama list` and GET /v1/models can disagree.
These tests pin that it reads the HTTP catalogue, matches either the official
Qwen tag or the Hugging Face GGUF alias, and treats SmolLM3 as present when
the daemon lists any smollm3 name.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_checker() -> Any:
    spec = importlib.util.spec_from_file_location(
        "check_local_ollama", ROOT / "scripts" / "check_local_ollama.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_local_ollama"] = module
    spec.loader.exec_module(module)
    return module


def test_matches_official_qwen_tag() -> None:
    module = load_checker()
    family = module.LOCAL_FAMILIES[0]
    assert module.match_family(family, frozenset({"qwen3:1.7b", "llama3.2:latest"})) == "qwen3:1.7b"


def test_matches_huggingface_qwen_gguf_alias() -> None:
    module = load_checker()
    family = module.LOCAL_FAMILIES[0]
    listed = frozenset({"hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0"})
    assert module.match_family(family, listed) == "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0"


def test_matches_smollm3_by_name_marker() -> None:
    module = load_checker()
    family = module.LOCAL_FAMILIES[1]
    listed = frozenset({"hf.co/ggml-org/SmolLM3-3B-GGUF:Q8_0"})
    assert module.match_family(family, listed) == "hf.co/ggml-org/SmolLM3-3B-GGUF:Q8_0"


def test_refuses_non_local_plaintext_base_url() -> None:
    module = load_checker()
    catalog = module.fetch_catalog("http://example.invalid/v1", timeout=1.0)
    assert catalog.error is not None
    assert "non-local plaintext" in catalog.error
    assert module.build_report(catalog)["status"] == "unreachable"
    module = load_checker()
    catalog = module.Catalog(
        base_url="http://127.0.0.1:11434/v1",
        openai_ids=(),
        ollama_names=(),
        error="connection refused",
    )
    report = module.build_report(catalog)
    assert report["status"] == "unreachable"
    assert report["missing_pulls"]


def test_partial_catalogue_is_status_missing() -> None:
    module = load_checker()
    catalog = module.Catalog(
        base_url="http://127.0.0.1:11434/v1",
        openai_ids=("llama3.2:latest", "gemma4:26b"),
        ollama_names=("llama3.2:latest", "gemma4:26b"),
    )
    report = module.build_report(catalog)
    assert report["status"] == "missing"
    assert [row["id"] for row in report["families"] if not row["present"]] == [
        "edge-qwen3-1.7b",
        "edge-smollm3-3b",
    ]
    text = module.render_text(report)
    assert "MISS Qwen3 1.7B" in text
    assert "$env:OLLAMA_HOST" in text
    assert "DIR-004" in text


def test_both_families_present_is_ok(capsys: Any) -> None:
    module = load_checker()
    catalog = module.Catalog(
        base_url="http://127.0.0.1:11434/v1",
        openai_ids=("qwen3:1.7b", "hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M"),
        ollama_names=("qwen3:1.7b", "hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M"),
    )
    with mock.patch.object(module, "fetch_catalog", return_value=catalog):
        code = module.main(["--json"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ok"
    assert all(row["present"] for row in payload["families"])
