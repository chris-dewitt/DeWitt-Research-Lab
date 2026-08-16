"""Regression tests for the Wix site auditor's detection logic.

The auditor previously reported ~35 false positives out of 40 findings against
the live site. These tests pin the four confirmed defects so they cannot return.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "audit_wix_site", ROOT / "scripts" / "audit_wix_site.py")
assert spec and spec.loader
audit = importlib.util.module_from_spec(spec)
sys.modules["audit_wix_site"] = audit
spec.loader.exec_module(audit)


DISCLOSURE = (
    "This is an independent initiative. "
    "Not a government, university, or accredited institution."
)


class TestTruthfulnessMatching:
    def test_required_disclosure_is_not_a_violation(self) -> None:
        """The independent-initiative disclosure is required content, not a gap."""
        assert audit.flag_untruthful(DISCLOSURE) == []

    def test_uppercase_disclosure_variant_is_not_a_violation(self) -> None:
        text = "INDEPENDENT INITIATIVE: NOT A GOVERNMENT, UNIVERSITY, OR ACCREDITED INSTITUTION."
        assert audit.flag_untruthful(text) == []

    def test_genuine_affiliation_claim_is_flagged(self) -> None:
        text = "DRL is accredited by the National Board and works with government agency partners."
        hits = audit.flag_untruthful(text)
        assert "accredited by" in hits

    def test_staff_scale_claim_is_flagged(self) -> None:
        assert "our team" in audit.flag_untruthful("Our team of researchers built this.")

    def test_disclaimer_does_not_mask_a_separate_sentence(self) -> None:
        text = f"{DISCLOSURE} Our team is enterprise-grade."
        hits = audit.flag_untruthful(text)
        assert "our team" in hits and "enterprise-grade" in hits


class TestThemeColorResolution:
    def test_resolves_wix_base_color_tokens(self) -> None:
        html = "<style>:root{--wst-base-1-color:#0B0B0C;--wst-base-2-color:#EDE6D6}</style>"
        canvas, foreground = audit.resolve_theme_colors(html)
        assert canvas == "#0B0B0C"
        assert foreground == "#EDE6D6"

    def test_falls_back_to_numbered_palette(self) -> None:
        html = "<style>:root{--color_11:11,11,12;--color_10:237,230,214}</style>"
        canvas, foreground = audit.resolve_theme_colors(html)
        assert canvas == "#0b0b0c"
        assert foreground == "#ede6d6"

    def test_cream_on_black_is_not_reported_as_light(self) -> None:
        """Incidental #fff on widgets must not outvote the resolved canvas."""
        html = (
            "<style>:root{--wst-base-1-color:#0B0B0C;--wst-base-2-color:#EDE6D6}</style>"
            + '<div style="background-color:#fff"></div>' * 18
        )
        canvas, _ = audit.resolve_theme_colors(html)
        assert canvas is not None
        assert audit.luminance(canvas) < 0.35


class TestSlugNormalisation:
    def test_hyphenated_live_slugs_match_approved_sections(self) -> None:
        import re

        paths = "/research-and-writing /projects /about-me"
        flat = re.sub(r"[-_]", "", paths)
        for slugs in audit.EXPECTED_TOP_SECTIONS.values():
            assert any(re.sub(r"[-_]", "", s) in flat for s in slugs), slugs


class TestPageTreeFollowsRES016:
    """The tree shrank when RES-016 made this a portfolio, not a workshop site.

    Scoring against the superseded eight-section plan produced eleven findings
    that pointed away from the approved site. These pin the contract so it
    cannot drift back.
    """

    def test_workshop_sections_are_no_longer_expected(self) -> None:
        for retired in ("Laboratory", "Teaching", "Failure Museum", "Status / Launch"):
            assert retired not in audit.EXPECTED_TOP_SECTIONS

    def test_the_approved_three_sections_are_expected(self) -> None:
        assert set(audit.EXPECTED_TOP_SECTIONS) == {"Research", "Projects", "About"}

    def test_hero_no_longer_requires_the_superseded_slogan(self) -> None:
        """RES-016: lead with the person, not a lab name or a slogan."""
        joined = " ".join(audit.REQUIRED_HOME_TEXT)
        assert "Christopher Noxon DeWitt" in joined
        assert "Workshop" not in joined
        assert "Intelligence for Good" not in joined

    def test_institutional_link_requirements_are_dropped(self) -> None:
        assert set(audit.REQUIRED_SITE_LINKS) == {"github", "privacy", "contact"}


class TestInstitutionalChrome:
    def test_operations_centre_framing_is_flagged(self) -> None:
        assert "specialist research nodes" in audit.flag_chrome(
            "Specialist research nodes designed for open-weight intelligence."
        )

    def test_uptime_framing_is_flagged(self) -> None:
        assert "uptime" in audit.flag_chrome("NODE: 01 // UPTIME: 99.9%")

    def test_ordinary_project_copy_is_not_flagged(self) -> None:
        text = "These are projects I use to study complex systems in practice."
        assert audit.flag_chrome(text) == []


class TestLookalikeSourceLinks:
    def test_hyphenated_github_domain_is_caught(self) -> None:
        """A typo here sends the source-code link to somebody else's domain."""
        hosts = audit.lookalike_github_hosts(["http://www.git-hub.com/chris-dewitt"])
        assert hosts == ["www.git-hub.com"]

    def test_real_github_links_pass(self) -> None:
        assert audit.lookalike_github_hosts(
            ["https://github.com/chris-dewitt", "https://www.github.com/chris-dewitt",
             "https://chris-dewitt.github.io/"]
        ) == []

    def test_unrelated_links_are_ignored(self) -> None:
        assert audit.lookalike_github_hosts(
            ["mailto:someone@example.com", "https://www.dewitt-labs.com/projects"]
        ) == []


class TestEvidenceForNumbers:
    def test_a_reported_percentage_is_surfaced(self) -> None:
        assert audit.PERCENT_CLAIM.findall("Deterministic pass rate achieved 94.2%") == ["94.2%"]

    def test_prose_without_numbers_is_quiet(self) -> None:
        assert audit.PERCENT_CLAIM.findall("The report documents its limitations.") == []
