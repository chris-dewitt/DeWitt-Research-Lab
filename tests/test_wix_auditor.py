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
    def test_hyphenated_live_slugs_match_expected_system_names(self) -> None:
        import re

        paths = "/atticus /atlas /fed-lens /balance-lab-ai /eval-forge"
        flat = re.sub(r"[-_]", "", paths)
        for system in audit.EXPECTED_SYSTEM_PAGES:
            assert re.sub(r"[-_]", "", system) in flat, system
