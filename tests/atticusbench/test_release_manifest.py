"""The release manifest must satisfy the canonical contract and be regenerable."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from atticusbench import load_corpus
from drl_ai_core import canonical_digest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from scripts.validate_atticusbench import (
    CASE_INDEX_PATH,
    DATASET_ID,
    DATASET_VERSION,
    RELEASE_DIR,
    artifact_digest,
    write_release_manifest,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = RELEASE_DIR / f"{DATASET_ID}-{DATASET_VERSION}.manifest.json"
CONTAMINATION_PATH = RELEASE_DIR / "contamination-report.json"


@pytest.fixture(scope="module")
def registry() -> Registry:
    resources = []
    for path in sorted((REPO_ROOT / "schemas").glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


@pytest.fixture(scope="module")
def manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_manifest_satisfies_the_canonical_schema(manifest, registry) -> None:
    schema = json.loads(
        (REPO_ROOT / "schemas/dataset-release-manifest.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.path))
    assert errors == [], [(list(error.path), error.message) for error in errors]


def test_manifest_digest_covers_its_own_content(manifest) -> None:
    payload = {key: value for key, value in manifest.items() if key != "manifest_digest"}
    assert manifest["manifest_digest"] == f"sha256:{canonical_digest(payload)}"


def test_every_referenced_artifact_exists_with_the_recorded_digest(manifest) -> None:
    references = [manifest["contamination_report"], *manifest["artifacts"]]
    for reference in references:
        assert reference["uri"].startswith("repo://")
        path = REPO_ROOT / reference["uri"].removeprefix("repo://")
        assert path.is_file(), reference["uri"]
        # Recomputed with the generator's own function rather than a second
        # copy of the hashing here. The copy was the reason this test could not
        # see that the digest depended on the checkout: it reproduced the raw
        # read it was meant to be checking, so the two agreed on Windows and on
        # Linux separately while disagreeing with each other.
        digest = artifact_digest(path, media_type=reference["media_type"])
        assert reference["digest"] == digest, reference["uri"]
        assert reference["classification"] == "public"


def test_manifest_counts_match_the_corpus(manifest) -> None:
    corpus = load_corpus()
    assert manifest["records"] == len(corpus.cases)
    assert manifest["splits"] == {"public-test": len(corpus.cases)}
    assert manifest["sources"][0]["corpus_digest"] == corpus.digest()
    review = manifest["review"]
    assert review["dual_human_review"] + review["single_human_review"] == len(corpus.cases)
    # The single-author caveat must travel with the manifest.
    assert "one person" in review["caveat"].lower()


def test_case_index_lists_every_case_and_fixture() -> None:
    corpus = load_corpus()
    index = json.loads(CASE_INDEX_PATH.read_text(encoding="utf-8"))
    assert index["corpus_digest"] == corpus.digest()
    assert set(index["cases"]) == {case.case_id for case in corpus.cases}
    assert set(index["fixtures"]) == {fixture.fixture_id for fixture in corpus.fixtures}
    for case in corpus.cases:
        entry = index["cases"][case.case_id]
        assert entry["digest"] == case.content_digest
        assert (REPO_ROOT / entry["path"]).is_file()


def test_contamination_report_declares_a_clean_corpus() -> None:
    report = json.loads(CONTAMINATION_PATH.read_text(encoding="utf-8"))
    assert report["duplication"]["clean"] is True
    assert report["known_contamination"] == []
    assert report["coverage"]["missing_families"] == []
    assert "unsuitable as a held-out measurement" in report["notes"]


def test_exactly_one_manifest_describes_the_tree() -> None:
    # A manifest whose digests match nothing in the tree is worse than no
    # manifest. Superseded releases live in git history, and the dataset card's
    # version history says what changed.
    manifests = sorted(RELEASE_DIR.glob("*.manifest.json"))
    assert [path.name for path in manifests] == [MANIFEST_PATH.name]


def test_regeneration_is_byte_identical() -> None:
    before = {
        path: path.read_bytes() for path in (MANIFEST_PATH, CONTAMINATION_PATH, CASE_INDEX_PATH)
    }
    write_release_manifest(load_corpus())
    for path, content in before.items():
        assert path.read_bytes() == content, path.name
