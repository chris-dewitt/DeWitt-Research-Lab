#!/usr/bin/env python
"""Validate the AtticusBench corpus and report its coverage and duplication.

Schema validation, cross-document consistency, content digests, family coverage,
and near-duplicate detection all run here. Nothing about this script measures a
system: it decides whether the dataset is fit to be measured against.

    uv run python scripts/validate_atticusbench.py
    uv run python scripts/validate_atticusbench.py --json
    uv run python scripts/validate_atticusbench.py --write-digests
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
for _relative in (
    "packages/drl-protocol/src",
    "packages/drl-ai-core/src",
    "services/atlas/src",
    "services/fedlens/src",
    "services/balancelab-ai/src",
    "services/evalforge/src",
    "services/atticus-control-plane/src",
    "datasets/atticusbench/src",
):
    sys.path.insert(0, str(REPO_ROOT / _relative))

import yaml  # noqa: E402
from atticusbench import (  # noqa: E402
    Corpus,
    CorpusError,
    content_digest,
    coverage_report,
    duplication_report,
    load_case,
    load_fixture,
)
from atticusbench.corpus import (  # noqa: E402
    consistency_problems,
    iter_case_paths,
    iter_fixture_paths,
)
from drl_ai_core import canonical_digest  # noqa: E402

DATASET_ID = "atticusbench-public-seed"
DATASET_VERSION = "0.1.1"
#: Release date of this seed. A constant, not the wall clock, so regenerating
#: the manifest on an unchanged corpus rewrites identical bytes.
RELEASE_TIMESTAMP = "2026-09-18T00:00:00Z"
RELEASE_DIR = REPO_ROOT / "datasets" / "atticusbench" / "release"
CASE_INDEX_PATH = RELEASE_DIR / "case-index.json"


def write_digests() -> list[str]:
    """Recompute and rewrite every recorded content digest.

    The digest covers the document with its own ``content_digest`` removed, so
    this is idempotent: running it twice changes nothing.
    """

    changed: list[str] = []
    for path in [*iter_fixture_paths(), *iter_case_paths()]:
        text = path.read_text(encoding="utf-8")
        document = yaml.safe_load(text)
        if not isinstance(document, dict):
            raise CorpusError(f"{path}: expected a YAML mapping")
        digest = content_digest(document)
        if document.get("content_digest") == digest:
            continue
        lines = [line for line in text.splitlines() if not line.startswith("content_digest:")]
        while lines and not lines[-1].strip():
            lines.pop()
        lines.append(f"content_digest: {digest}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        changed.append(str(path.relative_to(REPO_ROOT)))
    return changed


def load_without_consistency() -> Corpus:
    """Load every document so schema errors surface before consistency errors."""

    fixtures = tuple(load_fixture(path) for path in iter_fixture_paths())
    cases = tuple(load_case(path) for path in iter_case_paths())
    return Corpus(cases=cases, fixtures=fixtures)


#: Media types whose digest is taken over newline-normalized bytes.
#:
#: Every artifact this manifest names is text. Hashing it as it sits on disk
#: made the digest depend on the checkout: git stores LF, and a Windows clone
#: with ``core.autocrlf=true`` has CRLF in the working tree, so the same commit
#: produced two different manifests and the regeneration test failed on Windows
#: while CI stayed green. The dataset card claims this seed reproduces byte for
#: byte; hashing normalized bytes is what makes that true on every platform
#: rather than only on the one CI happens to run.
_TEXT_MEDIA_TYPES = frozenset(
    {"application/json", "application/schema+json", "application/yaml"}
)


def _is_text_media_type(media_type: str) -> bool:
    return media_type.startswith("text/") or media_type in _TEXT_MEDIA_TYPES


def artifact_digest(path: Path, *, media_type: str) -> str:
    """Digest one release artifact, normalizing line endings for text.

    A binary artifact is hashed byte for byte: normalizing it would corrupt the
    digest of any file where CR or LF is data rather than a line ending. Nothing
    in the current manifest is binary, and this branch exists so that adding one
    does not silently inherit text handling.
    """

    data = path.read_bytes()
    if _is_text_media_type(media_type):
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _artifact(
    *,
    identifier: str,
    kind: str,
    path: Path,
    media_type: str,
    title: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "id": identifier,
        "kind": kind,
        "uri": f"repo://{path.relative_to(REPO_ROOT).as_posix()}",
        "digest": artifact_digest(path, media_type=media_type),
        "classification": "public",
        "media_type": media_type,
        "title": title,
        "created_at": RELEASE_TIMESTAMP,
        "source_system": "dewitt-research-lab",
    }


def write_release_manifest(corpus: Corpus) -> list[Path]:
    """Write the contamination report and the dataset release manifest.

    The release date is a constant rather than the wall clock, so regenerating
    the manifest on an unchanged corpus rewrites identical bytes.
    """

    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    contamination = {
        "schema_version": "1.0.0",
        "dataset": DATASET_ID,
        "version": DATASET_VERSION,
        "method": (
            "Exact content digest, structural signature over fixture, mode, tool set, "
            "plan shape, invariants and expected terminal states, and Jaccard "
            "similarity over normalized request tokens. Detection does not run on "
            "text alone."
        ),
        "duplication": duplication_report(corpus),
        "coverage": coverage_report(corpus),
        "known_contamination": [],
        "notes": (
            "These cases are public and publish their expectations, so they are "
            "unsuitable as a held-out measurement for any system trained on this "
            "repository. No hidden-test material is stored in this tree."
        ),
    }
    contamination_path = RELEASE_DIR / "contamination-report.json"
    contamination_path.write_text(json.dumps(contamination, indent=2) + "\n", encoding="utf-8")

    index = {
        "schema_version": "1.0.0",
        "dataset": DATASET_ID,
        "version": DATASET_VERSION,
        "corpus_digest": corpus.digest(),
        "cases": {
            case.case_id: {
                "digest": case.content_digest,
                "family": case.family,
                "split": case.split,
                "mode": case.mode,
                "critical_suite": case.critical_suite,
                "environment_fixture": case.environment_fixture,
                "path": str(Path(case.source_path).relative_to(REPO_ROOT).as_posix()),
            }
            for case in corpus.cases
        },
        "fixtures": {
            fixture.fixture_id: {
                "digest": fixture.content_digest,
                "version": fixture.version,
                "clock": fixture.clock,
                "tools": list(fixture.tool_names),
                "path": str(Path(fixture.source_path).relative_to(REPO_ROOT).as_posix()),
            }
            for fixture in corpus.fixtures
        },
    }
    CASE_INDEX_PATH.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    artifacts = [
        _artifact(
            identifier="atticusbench-public-seed-cases",
            kind="dataset",
            path=CASE_INDEX_PATH,
            media_type="application/json",
            title="Case and fixture digest index",
        ),
        _artifact(
            identifier="atticusbench-public-seed-dataset-card",
            kind="document",
            path=REPO_ROOT / "datasets/atticusbench/docs/DATASET_CARD.md",
            media_type="text/markdown",
            title="Dataset card",
        ),
        _artifact(
            identifier="atticusbench-public-seed-case-schema",
            kind="document",
            path=REPO_ROOT / "datasets/atticusbench/schemas/atticusbench-case.schema.json",
            media_type="application/schema+json",
            title="Case schema",
        ),
        _artifact(
            identifier="atticusbench-public-seed-fixture-schema",
            kind="document",
            path=REPO_ROOT / "datasets/atticusbench/schemas/atticusbench-fixture.schema.json",
            media_type="application/schema+json",
            title="Fixture schema",
        ),
    ]
    results_path = REPO_ROOT / "runs/atticusbench/results.json"
    if results_path.exists():
        artifacts.append(
            _artifact(
                identifier="atticusbench-public-seed-baseline-results",
                kind="report",
                path=results_path,
                media_type="application/json",
                title="Deterministic baseline results",
            )
        )

    manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "id": DATASET_ID,
        "name": "AtticusBench Public Seed",
        "version": DATASET_VERSION,
        "released_at": RELEASE_TIMESTAMP,
        "license": {
            "id": "Apache-2.0",
            "uri": "repo://LICENSE",
            "content_rights": "synthetic, original to this repository",
        },
        "records": len(corpus.cases),
        "splits": {"public-test": len(corpus.cases)},
        "sources": [
            {
                "id": "hand-authored-synthetic",
                "description": (
                    "Hand-authored synthetic cases and fixtures. No model generated "
                    "a case, no donated trace was used, and no real record appears."
                ),
                "records": len(corpus.cases),
                "rights": "synthetic",
                "corpus_digest": corpus.digest(),
            }
        ],
        "review": {
            "dual_human_review": sum(
                1
                for case in corpus.cases
                if case.provenance.get("review_class") == "dual-human-review"
            ),
            "single_human_review": sum(
                1
                for case in corpus.cases
                if case.provenance.get("review_class") == "single-human-review"
            ),
            "automated_checks": [
                "schema validation",
                "cross-document consistency",
                "content digest verification",
                "duplication audit",
                "reference-plan execution against every case",
            ],
            "caveat": (
                "One person authored and reviewed this seed. The dual-review class "
                "records the specification's requirement, not two independent "
                "sign-offs."
            ),
        },
        "contamination_report": _artifact(
            identifier="atticusbench-public-seed-contamination",
            kind="report",
            path=contamination_path,
            media_type="application/json",
            title="Contamination and duplication report",
        ),
        "artifacts": artifacts,
    }
    manifest["manifest_digest"] = f"sha256:{canonical_digest(manifest)}"
    manifest_path = RELEASE_DIR / f"{DATASET_ID}-{DATASET_VERSION}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return [contamination_path, CASE_INDEX_PATH, manifest_path]


def build_report(corpus: Corpus) -> dict[str, Any]:
    problems = list(consistency_problems(corpus))
    coverage = coverage_report(corpus)
    duplication = duplication_report(corpus)
    return {
        "corpus_digest": corpus.digest(),
        "coverage": coverage,
        "duplication": duplication,
        "consistency_problems": problems,
        "valid": not problems and duplication["clean"] and not coverage["missing_families"],
    }


def render(report: dict[str, Any]) -> str:
    coverage = report["coverage"]
    duplication = report["duplication"]
    lines = [
        "AtticusBench corpus validation",
        f"  corpus digest        {report['corpus_digest']}",
        f"  cases                {coverage['cases']}",
        f"  fixtures             {coverage['fixtures']}",
        f"  critical-suite cases {coverage['critical_suite_cases']}",
        f"  public-session cases {coverage['public_session_cases']}",
        "",
        "Cases per family",
    ]
    for family, count in coverage["per_family"].items():
        lines.append(f"  {family:<28} {count}")
    lines.append("")
    lines.append("Perturbations")
    for perturbation, count in coverage["perturbations"].items():
        lines.append(f"  {perturbation:<28} {count}")
    lines.append("")
    lines.append(
        "Duplication: "
        + (
            "clean"
            if duplication["clean"]
            else (
                f"{len(duplication['near_duplicate_requests'])} near-duplicate request pair(s), "
                f"{len(duplication['identical_structure'])} identical-structure group(s)"
            )
        )
    )
    if coverage["missing_families"]:
        lines.append("Missing families: " + ", ".join(coverage["missing_families"]))
    if report["consistency_problems"]:
        lines.append("")
        lines.append("Consistency problems")
        for problem in report["consistency_problems"]:
            lines.append(f"  - {problem}")
    lines.append("")
    lines.append("RESULT: " + ("valid" if report["valid"] else "invalid"))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-digests",
        action="store_true",
        help="recompute and rewrite content digests, then validate",
    )
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="write the case index, contamination report, and dataset release manifest",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument("--out", type=Path, help="also write the report to this path")
    args = parser.parse_args(argv)

    if args.write_digests:
        for relative in write_digests():
            print(f"digest updated: {relative}")

    try:
        corpus = load_without_consistency()
    except CorpusError as exc:
        print(f"corpus failed to load: {exc}", file=sys.stderr)
        return 2

    report = build_report(corpus)
    if args.write_manifest:
        if not report["valid"]:
            print("refusing to write a manifest for an invalid corpus", file=sys.stderr)
            return 1
        for written in write_release_manifest(corpus):
            print(f"wrote {written.relative_to(REPO_ROOT)}")

    payload = json.dumps(report, indent=2) if args.json else render(report)
    print(payload)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
