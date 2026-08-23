#!/usr/bin/env python3
"""Show which models the daemon Atticus talks to actually has.

``ollama list`` and ``GET http://localhost:11434/v1/models`` can disagree on
Windows when the CLI and the app keep separate libraries. Atticus uses the
HTTP catalogue. This script reads that catalogue and reports whether the
Director's local pair is present: Qwen3 1.7B GGUF and SmolLM3-3B.

    uv run python scripts/check_local_ollama.py
    uv run python scripts/check_local_ollama.py --base-url http://127.0.0.1:11434/v1

Exit status:
  0  both expected families are listed
  1  the endpoint did not answer
  2  the endpoint answered but at least one expected family is missing
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "http://localhost:11434/v1"
REGISTER = REPO_ROOT / "models" / "bakeoff" / "candidates.yaml"

# Expected local workstation tags. Aliases cover the Hugging Face GGUF pull
# the Director already ran on a different Ollama library.
LOCAL_FAMILIES: tuple[dict[str, Any], ...] = (
    {
        "id": "edge-qwen3-1.7b",
        "label": "Qwen3 1.7B",
        "preferred": "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0",
        "aliases": (
            "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0",
            "qwen3:1.7b",
            "qwen3:1.7b-q4_K_M",
        ),
        "pull": "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0",
        "no_thinking": True,
    },
    {
        "id": "edge-smollm3-3b",
        "label": "SmolLM3 3B",
        "preferred": "hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M",
        "aliases": ("hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M",),
        "name_markers": ("smollm3", "smol-lm3"),
        "pull": "hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M",
        "no_thinking": True,
    },
)


@dataclass(frozen=True, slots=True)
class Catalog:
    base_url: str
    openai_ids: tuple[str, ...]
    ollama_names: tuple[str, ...]
    error: str | None = None

    @property
    def ids(self) -> frozenset[str]:
        return frozenset(self.openai_ids) | frozenset(self.ollama_names)

    @property
    def reachable(self) -> bool:
        return self.error is None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--base-url",
        default=os.environ.get("ATTICUS_MODEL_BASE_URL", "").strip() or DEFAULT_BASE_URL,
        help="OpenAI-compatible base URL Atticus will use",
    )
    parser.add_argument("--json", action="store_true", help="Print a machine-readable report")
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Seconds to wait for the catalogue",
    )
    return parser


def _get_json(url: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(url, method="GET")  # noqa: S310
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310  # nosec B310
        body = response.read().decode("utf-8", "replace")
    parsed = json.loads(body)
    if not isinstance(parsed, dict):
        raise ValueError(f"{url} returned a non-object")
    return parsed


def origin_of(base_url: str) -> str:
    """Return scheme://host:port from an OpenAI-compatible base URL."""
    trimmed = base_url.rstrip("/")
    if trimmed.endswith("/v1"):
        trimmed = trimmed[: -len("/v1")]
    return trimmed


def fetch_catalog(base_url: str, timeout: float) -> Catalog:
    """Read GET /v1/models and, when present, GET /api/tags."""
    if not base_url.startswith(("http://localhost", "http://127.0.0.1", "https://")):
        return Catalog(
            base_url=base_url,
            openai_ids=(),
            ollama_names=(),
            error=f"refusing non-local plaintext endpoint: {base_url}",
        )
    openai_ids: list[str] = []
    ollama_names: list[str] = []
    models_url = f"{base_url.rstrip('/')}/models"
    try:
        listing = _get_json(models_url, timeout)
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
        return Catalog(base_url=base_url, openai_ids=(), ollama_names=(), error=str(exc))
    data = listing.get("data")
    if isinstance(data, list):
        openai_ids = [
            str(entry["id"])
            for entry in data
            if isinstance(entry, dict) and isinstance(entry.get("id"), str)
        ]
    tags_url = f"{origin_of(base_url)}/api/tags"
    try:
        tags = _get_json(tags_url, timeout)
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError):
        tags = {}
    models = tags.get("models")
    if isinstance(models, list):
        for row in models:
            if not isinstance(row, dict):
                continue
            name = row.get("name") or row.get("model")
            if isinstance(name, str) and name:
                ollama_names.append(name)
    return Catalog(
        base_url=base_url,
        openai_ids=tuple(openai_ids),
        ollama_names=tuple(ollama_names),
    )


def match_family(family: dict[str, Any], ids: frozenset[str]) -> str | None:
    """Return the listed tag that satisfies a family, if any."""
    aliases = {str(tag) for tag in family.get("aliases", ())}
    aliases.add(str(family["preferred"]))
    exact = aliases & set(ids)
    if exact:
        # Prefer the register's serving tag when both an official and GGUF tag exist.
        preferred = str(family["preferred"])
        if preferred in exact:
            return preferred
        return sorted(exact)[0]
    markers = tuple(str(item).lower() for item in family.get("name_markers", ()))
    if not markers:
        return None
    for listed in sorted(ids):
        lowered = listed.lower()
        if any(marker in lowered for marker in markers):
            return listed
    return None


def powershell_env(model: str, *, no_thinking: bool) -> list[str]:
    lines = [
        '$env:OLLAMA_HOST="http://127.0.0.1:11434"',
        f'$env:ATTICUS_MODEL="{model}"',
    ]
    if no_thinking:
        lines.append('$env:ATTICUS_MODEL_NO_THINKING="1"')
    return lines


def bash_env(model: str, *, no_thinking: bool) -> list[str]:
    lines = [
        "export OLLAMA_HOST=http://127.0.0.1:11434",
        f"export ATTICUS_MODEL={model}",
    ]
    if no_thinking:
        lines.append("export ATTICUS_MODEL_NO_THINKING=1")
    return lines


def build_report(catalog: Catalog) -> dict[str, Any]:
    families = []
    missing_pulls: list[str] = []
    for family in LOCAL_FAMILIES:
        matched = None if not catalog.reachable else match_family(family, catalog.ids)
        families.append(
            {
                "id": family["id"],
                "label": family["label"],
                "preferred": family["preferred"],
                "matched": matched,
                "present": matched is not None,
                "no_thinking": bool(family["no_thinking"]),
                "pull": family["pull"],
            }
        )
        if matched is None:
            missing_pulls.append(str(family["pull"]))
    status = "ok"
    if not catalog.reachable:
        status = "unreachable"
    elif missing_pulls:
        status = "missing"
    return {
        "status": status,
        "base_url": catalog.base_url,
        "error": catalog.error,
        "openai_ids": list(catalog.openai_ids),
        "ollama_names": list(catalog.ollama_names),
        "families": families,
        "missing_pulls": missing_pulls,
        "register": str(REGISTER.relative_to(REPO_ROOT)),
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [
        f"Atticus endpoint: {report['base_url']}",
        "This listing is GET /v1/models (and /api/tags when present).",
        '`ollama list` is only trustworthy after: $env:OLLAMA_HOST="http://127.0.0.1:11434"',
        "",
    ]
    listed = report["openai_ids"] or report["ollama_names"]
    if report["status"] == "unreachable":
        lines.append(f"UNREACHABLE: {report['error']}")
        lines.append("Is the Ollama app running? Try: curl.exe http://127.0.0.1:11434/v1/models")
        return "\n".join(lines)

    lines.append("Daemon tags:")
    if listed:
        for name in listed:
            lines.append(f"  - {name}")
    else:
        lines.append("  (none)")
    lines.append("")
    lines.append("Expected local Atticus models:")
    for family in report["families"]:
        if family["present"]:
            lines.append(f"  OK   {family['label']}: {family['matched']}")
        else:
            lines.append(f"  MISS {family['label']}: pull {family['pull']}")

    if report["missing_pulls"]:
        lines.extend(
            [
                "",
                "Pin the CLI to this daemon, then pull:",
                '  $env:OLLAMA_HOST="http://127.0.0.1:11434"',
            ]
        )
        for tag in report["missing_pulls"]:
            lines.append(f"  ollama pull {tag}")
        lines.append("  curl.exe http://127.0.0.1:11434/api/tags")

    first_present = next((row for row in report["families"] if row["present"]), None)
    if first_present is not None:
        model = str(first_present["matched"])
        lines.extend(
            [
                "",
                "Run Atticus against the first present model (PowerShell):",
                *[
                    f"  {line}"
                    for line in powershell_env(model, no_thinking=first_present["no_thinking"])
                ],
                "  uv run python scripts/probe_model.py --model "
                + model
                + (" --no-thinking" if first_present["no_thinking"] else ""),
                "  uv run --package atticus-control-plane atticus-demo --public",
                "PLANNER must say 'model planner via'. Anything else is a fallback.",
            ]
        )
    lines.extend(
        [
            "",
            "These are workstation/edge tags. They do not select Atticus Core or "
            "Edge (DIR-004: which models fill those roles; still open).",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    catalog = fetch_catalog(args.base_url, args.timeout)
    report = build_report(catalog)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report))
    if report["status"] == "unreachable":
        return 1
    if report["status"] == "missing":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
