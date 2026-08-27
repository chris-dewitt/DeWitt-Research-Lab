"""Tests for the static replay viewer.

The important assertions are about honesty: an unverified bundle must not render,
the degraded run must be visibly marked as degraded, and the demo-key caveat must
appear on every page. A viewer that silently renders a tampered recording is
worse than no viewer, because it lends provenance to content that has none.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from evalforge_service.replay_site import (
    ReplayBundle,
    ReplaySiteError,
    build_site,
    load_bundle,
    render_bundle_page,
    render_index,
    site_metadata,
)

ROOT = Path(__file__).resolve().parents[1]
BUNDLES = ROOT / "services" / "evalforge" / "fixtures" / "signed_replays"


@pytest.fixture
def success() -> ReplayBundle:
    return load_bundle(BUNDLES / "success")


@pytest.fixture
def degraded() -> ReplayBundle:
    return load_bundle(BUNDLES / "degraded")


class TestLoading:
    def test_loads_the_success_bundle(self, success: ReplayBundle) -> None:
        assert success.name == "success"
        assert success.trace
        assert success.final_state == "completed"
        assert not success.degraded

    def test_loads_the_degraded_bundle(self, degraded: ReplayBundle) -> None:
        assert degraded.degraded
        assert degraded.final_state == "degraded"
        assert degraded.failures, "degraded bundle should record a tool failure"

    def test_evidence_and_limitations_are_read_from_the_run(self, success: ReplayBundle) -> None:
        assert success.evidence_ids
        assert success.limitations
        assert success.maturity == "prototype"

    def test_missing_directory_is_an_error(self, tmp_path: Path) -> None:
        with pytest.raises(ReplaySiteError, match="not a bundle directory"):
            load_bundle(tmp_path / "nope")

    def test_tampered_bundle_is_refused(self, tmp_path: Path) -> None:
        """The headline guard: altering a recording must stop it rendering."""
        target = tmp_path / "success"
        shutil.copytree(BUNDLES / "success", target)
        summary = json.loads((target / "task-summary.json").read_text())
        summary["evidence_ids"] = ["fabricated-evidence"]
        (target / "task-summary.json").write_text(json.dumps(summary))

        with pytest.raises(ReplaySiteError, match="refusing to render unverified"):
            load_bundle(target)

    def test_missing_artifact_is_an_error(self, tmp_path: Path) -> None:
        target = tmp_path / "success"
        shutil.copytree(BUNDLES / "success", target)
        (target / "execution-trace.json").unlink()
        with pytest.raises(ReplaySiteError):
            load_bundle(target)


class TestRendering:
    def test_page_is_self_contained(self, success: ReplayBundle) -> None:
        """No external requests: the page must work offline and under a strict CSP."""
        page = render_bundle_page(success)
        assert "<style>" in page
        for marker in ("http://", "src=", "cdn", "<script"):
            assert marker not in page.lower(), f"page should not reference {marker!r}"

    def test_page_shows_every_trace_event(self, degraded: ReplayBundle) -> None:
        page = render_bundle_page(degraded)
        for event in degraded.trace:
            assert str(event["event_type"]) in page

    def test_degraded_page_marks_the_failure(self, degraded: ReplayBundle) -> None:
        page = render_bundle_page(degraded)
        assert "failed partway through" in page
        assert "is-failure" in page
        assert "tag-bad" in page

    def test_success_page_is_not_marked_degraded(self, success: ReplayBundle) -> None:
        page = render_bundle_page(success)
        assert "failed partway through" not in page
        assert "tag-ok" in page

    def test_demo_key_caveat_is_present(self, success: ReplayBundle) -> None:
        """Structural integrity is real; the signing identity is not production."""
        page = render_bundle_page(success)
        assert "demo key" in page
        assert "not a production signing identity" in page

    def test_limitations_are_rendered(self, success: ReplayBundle) -> None:
        page = render_bundle_page(success)
        for limitation in success.limitations:
            assert limitation[:40] in page

    def test_evidence_lineage_is_rendered(self, success: ReplayBundle) -> None:
        page = render_bundle_page(success)
        for name in success.linked_workflow.get("links", {}):
            assert name in page

    def test_laboratory_identity_and_disclosure_on_every_page(
        self, success: ReplayBundle, degraded: ReplayBundle
    ) -> None:
        for page in (
            render_bundle_page(success),
            render_bundle_page(degraded),
            render_index([success, degraded]),
        ):
            assert "DeWitt Research Laboratory" in page
            assert "Christopher Noxon DeWitt" in page
            assert "www.dewitt-labs.com" in page
            assert "Independent personal research artifact" in page
            assert "does not endorse this project" in page

    def test_every_page_has_accessible_document_landmarks(
        self, success: ReplayBundle, degraded: ReplayBundle
    ) -> None:
        for page in (
            render_bundle_page(success),
            render_bundle_page(degraded),
            render_index([success, degraded]),
        ):
            assert 'class="skip-link" href="#main"' in page
            assert '<header class="site-header">' in page
            assert '<nav class="site-nav" aria-label="Primary">' in page
            assert '<main id="main" class="shell" tabindex="-1">' in page
            assert '<footer class="site-footer">' in page

    def test_run_tables_are_captioned_scoped_and_keyboard_reachable(
        self, success: ReplayBundle
    ) -> None:
        page = render_bundle_page(success)
        assert page.count('class="table-region" tabindex="0" role="region"') == 2
        assert "<caption>Specialist artifacts linked to this recorded run</caption>" in page
        assert "<caption>Recorded execution and integrity metadata</caption>" in page
        assert 'scope="col"' in page
        assert 'scope="row"' in page

    def test_status_is_not_communicated_by_color_alone(
        self, success: ReplayBundle, degraded: ReplayBundle
    ) -> None:
        success_page = render_bundle_page(success)
        degraded_page = render_bundle_page(degraded)
        assert ">completed<" in success_page
        assert ">degraded<" in degraded_page
        assert "This run failed partway through and kept going" in degraded_page

    def test_index_links_each_bundle(self, success: ReplayBundle, degraded: ReplayBundle) -> None:
        index = render_index([success, degraded])
        assert 'href="success.html"' in index
        assert 'href="degraded.html"' in index

    def test_index_states_prototype_maturity(
        self, success: ReplayBundle, degraded: ReplayBundle
    ) -> None:
        index = render_index([success, degraded])
        assert "prototype" in index
        assert "fixture" in index
        assert "demo signing key" in index
        assert "www.dewitt-labs.com" in index

    def test_html_is_escaped(self, success: ReplayBundle) -> None:
        hostile = ReplayBundle(
            name="x",
            manifest=success.manifest,
            trace=({"event_type": "t", "state": "s", "message": "<script>bad()</script>"},),
            summary={"evidence_ids": [], "limitations": []},
            linked_workflow={"links": {}, "maturity": "prototype"},
            evaluation={},
        )
        page = render_bundle_page(hostile)
        assert "<script>bad()" not in page
        assert "&lt;script&gt;" in page


class TestBuild:
    def test_builds_all_pages(self, tmp_path: Path) -> None:
        written = build_site(BUNDLES, tmp_path)
        names = {p.name for p in written}
        assert names == {"index.html", "success.html", "degraded.html"}
        assert all(p.exists() and p.stat().st_size > 0 for p in written)

    def test_success_is_ordered_before_degraded(self, tmp_path: Path) -> None:
        build_site(BUNDLES, tmp_path)
        index = (tmp_path / "index.html").read_text()
        assert index.index("success.html") < index.index("degraded.html")

    def test_missing_root_is_an_error(self, tmp_path: Path) -> None:
        with pytest.raises(ReplaySiteError, match="bundles root not found"):
            build_site(tmp_path / "nope", tmp_path / "out")

    def test_empty_root_fails_loudly(self, tmp_path: Path) -> None:
        """A misconfigured path must not publish an empty site."""
        empty = tmp_path / "empty"
        empty.mkdir()
        with pytest.raises(ReplaySiteError, match="no replay bundles"):
            build_site(empty, tmp_path / "out")

    def test_build_is_reproducible(self, tmp_path: Path) -> None:
        a, b = tmp_path / "a", tmp_path / "b"
        build_site(BUNDLES, a)
        build_site(BUNDLES, b)
        for name in ("index.html", "success.html", "degraded.html"):
            assert (a / name).read_text(encoding="utf-8") == (b / name).read_text(encoding="utf-8")

    def test_metadata_describes_what_was_published(
        self, success: ReplayBundle, degraded: ReplayBundle
    ) -> None:
        meta = site_metadata([success, degraded])
        assert meta["bundle_count"] == 2
        states = {b["name"]: b["degraded"] for b in meta["bundles"]}
        assert states == {"success": False, "degraded": True}
