"""Federal Reserve monetary-policy press RSS."""

from __future__ import annotations

import re
from datetime import UTC, date, datetime
from email.utils import parsedate_to_datetime
from typing import Any

from drl_ai_core import canonical_digest

FED_MONETARY_RSS = "https://www.federalreserve.gov/feeds/press_monetary.xml"
_TAG_RE = re.compile(r"<[^>]+>")
_ITEM_RE = re.compile(r"<item>(.*?)</item>", flags=re.S | re.I)


def _strip_html(text: str) -> str:
    cleaned = _TAG_RE.sub(" ", text)
    return " ".join(cleaned.split()).strip()


def _tag(block: str, name: str) -> str:
    match = re.search(rf"<{name}[^>]*>(.*?)</{name}>", block, flags=re.S | re.I)
    if not match:
        return ""
    text = match.group(1).strip()
    cdata = re.fullmatch(r"<!\[CDATA\[(.*)\]\]>", text, flags=re.S)
    return cdata.group(1).strip() if cdata else text


def _item_date(pub_date: str) -> date:
    try:
        parsed = parsedate_to_datetime(pub_date)
    except (TypeError, ValueError):
        return datetime.now(UTC).date()
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.date()


def parse_fed_monetary_rss(xml_text: str, *, limit: int = 8) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for block in _ITEM_RE.findall(xml_text)[:limit]:
        title = _strip_html(_tag(block, "title"))
        link = _tag(block, "link")
        description = _strip_html(_tag(block, "description"))
        guid = _tag(block, "guid") or link or title
        published = _item_date(_tag(block, "pubDate"))
        if not title or not description:
            continue
        digest = canonical_digest(guid)[:12]
        items.append(
            {
                "document_id": f"fed-press-{published.isoformat()}-{digest}",
                "title": title,
                "published_date": published.isoformat(),
                "text": f"{title}. {description}",
                "citation": link or FED_MONETARY_RSS,
                "source_id": "federal-reserve-press-monetary",
            }
        )
    items.sort(key=lambda item: item["published_date"])
    return items
