"""Official public-feed pipeline: parse, store, change, and opt-in wiring."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from atlas_service import AtlasService
from atticus_control_plane.runtime import build_local_runtime, live_data_enabled
from drl_protocol import TaskRequest
from fedlens_service import FedLensService

from scripts.public_feeds.changes import compute_series_changes
from scripts.public_feeds.fed_rss import parse_fed_monetary_rss
from scripts.public_feeds.fred import parse_fred_observations
from scripts.public_feeds.http import FeedFetchError, require_allowed_url
from scripts.public_feeds.refresh import refresh_public_feeds
from scripts.public_feeds.treasury import parse_treasury_csv


def test_yahoo_and_http_hosts_are_refused() -> None:
    with pytest.raises(FeedFetchError, match="allowlist"):
        require_allowed_url("https://query1.finance.yahoo.com/v8/finance/chart/SPY")
    with pytest.raises(FeedFetchError, match="non-HTTPS"):
        require_allowed_url("http://api.stlouisfed.org/fred/series")


def test_fred_parser_skips_missing_prints() -> None:
    payload = {
        "observations": [
            {"date": "2026-06-01", "value": "."},
            {"date": "2026-07-01", "value": "3.20"},
            {"date": "2026-08-01", "value": "3.10"},
        ]
    }
    items = parse_fred_observations("CPI_YOY", payload)
    assert [item["value"] for item in items] == ["3.20", "3.10"]
    assert items[-1]["citation"].startswith("https://fred.stlouisfed.org/series/CPIAUCSL")


def test_treasury_csv_maps_two_and_ten_year() -> None:
    csv_text = "Date,2 Yr,10 Yr\n08/21/2026,3.70,4.20\n08/22/2026,3.71,4.22\n"
    items = parse_treasury_csv(csv_text)
    assert {item["series_id"] for item in items} == {"UST_2Y", "UST_10Y"}
    tens = [item for item in items if item["series_id"] == "UST_10Y"]
    assert tens[-1]["value"] == "4.22"
    assert tens[-1]["observation_date"] == "2026-08-22"


def test_fed_rss_requires_two_items_and_strips_html() -> None:
    xml = """<?xml version="1.0"?>
    <rss><channel>
      <item>
        <title>Earlier statement</title>
        <link>https://www.federalreserve.gov/a.htm</link>
        <guid>a</guid>
        <pubDate>Wed, 06 May 2026 14:00:00 GMT</pubDate>
        <description>&lt;p&gt;Inflation remains elevated.&lt;/p&gt;</description>
      </item>
      <item>
        <title>Latest statement</title>
        <link>https://www.federalreserve.gov/b.htm</link>
        <guid>b</guid>
        <pubDate>Wed, 17 Jun 2026 14:00:00 GMT</pubDate>
        <description>Activity is slowing. Risks appear more balanced.</description>
      </item>
    </channel></rss>
    """
    docs = parse_fed_monetary_rss(xml)
    assert len(docs) == 2
    assert "elevated" in docs[0]["text"]
    assert "<p>" not in docs[0]["text"]
    assert docs[0]["published_date"] == "2026-05-06"


def test_series_changes_use_the_last_two_prints() -> None:
    changes = compute_series_changes(
        [
            {"series_id": "UST_10Y", "value": "4.20", "observation_date": "2026-08-21"},
            {"series_id": "UST_10Y", "value": "4.22", "observation_date": "2026-08-22"},
            {"series_id": "CPI_YOY", "value": "3.10", "observation_date": "2026-07-01"},
        ]
    )
    assert len(changes) == 1
    assert changes[0]["series_id"] == "UST_10Y"
    assert changes[0]["delta"] == "0.02"


def test_refresh_writes_store_from_injected_fetch(tmp_path: Path) -> None:
    fred = {
        "observations": [
            {"date": "2026-07-01", "value": "3.10"},
            {"date": "2026-08-01", "value": "3.00"},
        ]
    }
    csv_text = "Date,2 Yr,10 Yr\n08/21/2026,3.70,4.20\n08/22/2026,3.71,4.22\n"
    rss = """<?xml version="1.0"?><rss><channel>
      <item><title>One</title><link>https://www.federalreserve.gov/1</link>
      <guid>1</guid><pubDate>Wed, 06 May 2026 14:00:00 GMT</pubDate>
      <description>Inflation remains elevated.</description></item>
      <item><title>Two</title><link>https://www.federalreserve.gov/2</link>
      <guid>2</guid><pubDate>Wed, 17 Jun 2026 14:00:00 GMT</pubDate>
      <description>Activity is slowing.</description></item>
    </channel></rss>"""

    def fake_fetch(url: str) -> str:
        if "stlouisfed" in url:
            return json.dumps(fred)
        if "treasury.gov" in url:
            return csv_text
        if "federalreserve.gov" in url:
            return rss
        raise AssertionError(url)

    status = refresh_public_feeds(
        root=tmp_path, fred_api_key="test-key-not-secret", fetch=fake_fetch
    )
    assert status["yahoo_finance"] == "rejected:terms-of-use"
    assert status["observation_count"] >= 4
    assert status["document_count"] == 2
    assert status["change_count"] >= 1
    atlas = AtlasService.from_feed_store(tmp_path)
    snap = atlas.research_snapshot(as_of=date(2026, 8, 22))
    assert {item.series_id for item in snap} >= {"CPI_YOY", "UST_2Y", "UST_10Y"}
    changes = atlas.series_changes(as_of=date(2026, 8, 22))
    assert any(row["series_id"] == "CPI_YOY" and row["delta"] == "-0.10" for row in changes)
    fed = FedLensService.from_feed_store(tmp_path)
    assert fed.latest(as_of=date(2026, 6, 17)).title == "Two"


def test_live_runtime_reads_the_store_and_reports_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    refresh_public_feeds(
        root=tmp_path,
        fred_api_key="",
        fetch=lambda url: (
            "Date,2 Yr,10 Yr\n08/21/2026,3.70,4.20\n08/22/2026,3.71,4.22\n"
            if "treasury.gov" in url
            else """<?xml version="1.0"?><rss><channel>
      <item><title>One</title><link>https://www.federalreserve.gov/1</link>
      <guid>1</guid><pubDate>Wed, 06 May 2026 14:00:00 GMT</pubDate>
      <description>Inflation remains elevated.</description></item>
      <item><title>Two</title><link>https://www.federalreserve.gov/2</link>
      <guid>2</guid><pubDate>Wed, 17 Jun 2026 14:00:00 GMT</pubDate>
      <description>Activity is slowing.</description></item>
    </channel></rss>"""
        ),
    )
    monkeypatch.setenv("ATTICUS_LIVE_DATA", "1")
    monkeypatch.setenv("DRL_FEED_ROOT", str(tmp_path))
    monkeypatch.delenv("ATTICUS_MODEL", raising=False)
    assert live_data_enabled() is True
    result = build_local_runtime().run(
        TaskRequest(
            "live-feed-test",
            "Use inflation and Federal Reserve evidence to run a bear-steepener bank scenario",
            public_session=True,
            as_of="2026-08-22",
        )
    )
    assert result.state.value == "completed"
    assert result.artifacts.get("series_changes")
    blob = " ".join(result.limitations)
    assert "official public" in blob
    assert "ATTICUS_LIVE_DATA=1" in blob
    assert "ADR-0010" not in blob
    assert "DRL-019" not in blob
    assert result.summary.startswith("Public data shows")
    assert "synthetic communication" not in result.summary
    assert "“Two”" in result.summary or "“One”" in result.summary
    atlas_items = [item for item in result.evidence if item.evidence_id.startswith("atlas-")]
    assert atlas_items
    assert all(not item.citation.startswith("fixture://") for item in atlas_items)


def test_default_runtime_stays_on_fixtures(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ATTICUS_LIVE_DATA", raising=False)
    monkeypatch.delenv("ATTICUS_MODEL", raising=False)
    result = build_local_runtime().run(
        TaskRequest(
            "fixture-still",
            "Use inflation and Federal Reserve evidence to run a bear-steepener bank scenario",
            public_session=True,
            as_of="2026-07-24",
        )
    )
    assert result.state.value == "completed"
    assert len(result.evidence) == 5
    assert any("canned fixtures" in item or "synthetic" in item for item in result.limitations)
    assert not any("ADR-0010" in item for item in result.limitations)
