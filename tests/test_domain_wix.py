from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_domain_routing_contract():
    data = yaml.safe_load((ROOT / "configs/domain-routing.yaml").read_text())
    assert data["canonical_origin"] == "https://www.dwit-labs.com"
    assert data["institutional_site"]["platform"] == "Wix"
    assert data["policies"]["primary_apps_embedded_in_wix"] is False
    assert any(x["host"] == "atticus.dwit-labs.com" for x in data["applications"])


def test_wix_specs_exist():
    assert (ROOT / "docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md").exists()
    assert (ROOT / "docs/08-web-brand/WIX_SITE_BUILD_PLAN.md").exists()
    assert (ROOT / "docs/07-platform-gcp/DOMAIN_DNS_AND_WIX_RUNBOOK.md").exists()
