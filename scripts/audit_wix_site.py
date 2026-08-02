#!/usr/bin/env python3
"""Read-only audit of the live Wix site against approved DRL web specs.

Compares www.dewitt-labs.com and its Wix CMS collections against:
- docs/08-web-brand/BRAND_SYSTEM.md (cream-on-black, prohibited motifs, voice)
- docs/08-web-brand/WIX_SITE_BUILD_PLAN.md (page tree, homepage composition,
  CMS collections, required pre-publication content)
- docs/08-web-brand/WIX_EDITOR_HANDOFF_CHECKLIST.md (domain, structure, truthful
  maturity labels)
- docs/09-open-source/OPEN_SOURCE_MATURITY_MODEL.md (allowed maturity vocabulary)

Environment:
  WIX_API_KEY      required for CMS checks (Authorization header, never printed)
  WIX_SITE_ID      optional; skips site discovery when set
  WIX_ACCOUNT_ID   optional; some account-level endpoints require it

Usage:
  python scripts/audit_wix_site.py [--out report.md] [--max-pages 30]

Only query/GET endpoints are used. Nothing on the site is created, updated,
or deleted, and the API key is never written to output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser

SITE_HOST = "www.dewitt-labs.com"
APEX_HOST = "dewitt-labs.com"
API_BASE = "https://www.wixapis.com"

EXPECTED_COLLECTIONS = [
    "Systems",
    "ResearchArtifacts",
    "OpenArtifacts",
    "TeachingResources",
    "FailureRecords",
    "PeopleAndContributors",
    "Announcements",
    "ExternalLaunchTargets",
]

# Approved page tree (WIX_SITE_BUILD_PLAN.md) as slug fragments to look for in
# the sitemap. The plan allows shallow initial sections, so top-level sections
# are GAPs when missing while sub-pages are NOTEs.
EXPECTED_TOP_SECTIONS = {
    "Laboratory": ["laboratory", "lab"],
    "Systems": ["systems", "system"],
    "Research": ["research"],
    "Open Source": ["open-source", "opensource", "open_source"],
    "Teaching": ["teaching", "learn"],
    "Failure Museum": ["failure-museum", "failure"],
    "About": ["about"],
    "Status / Launch": ["status", "launch"],
}
EXPECTED_SYSTEM_PAGES = ["atticus", "atlas", "fedlens", "balancelab", "evalforge"]

# Required homepage text (hero hierarchy + founder line).
REQUIRED_HOME_TEXT = [
    "DeWitt Research Laboratory",
    "Independent research in open and applied intelligence",
    "AI for Good. AI for all.",
    "Intelligence of the people and for the people.",
    "Christopher Noxon DeWitt",
]

# Required pre-publication links/content anywhere on the site.
REQUIRED_SITE_LINKS = ["github", "privacy", "contact", "governance", "security", "status"]

# Allowed maturity vocabulary (OPEN_SOURCE_MATURITY_MODEL.md) plus truthful
# planned-state wording from the build plan.
ALLOWED_MATURITY = {
    "incubator", "experimental", "alpha", "beta", "stable",
    "deprecated", "archived", "planned", "prototype", "research preview",
}

# Language that implies institutional history, staff scale, or production
# maturity DRL does not have (BRAND_SYSTEM.md voice + handoff checklist).
UNTRUTHFUL_TERMS = [
    "our team", "our staff", "our scientists", "our engineers",
    "accredited", "university", "government", "federally",
    "production-ready", "enterprise-grade", "battle-tested",
    "trusted by", "clients include", "award-winning", "industry-leading",
    "world-class", "patented", "99.9%", "uptime guarantee",
]

findings: list[tuple[str, str, str]] = []  # (severity, area, message)


def add(severity: str, area: str, message: str) -> None:
    findings.append((severity, area, message))


def http(url: str, *, body: dict | None = None, headers: dict | None = None,
         follow_redirects: bool = True, timeout: int = 30):
    """GET (or POST when body given) returning (status, headers, text)."""
    if not url.startswith("https://"):
        raise ValueError(f"refusing non-https URL: {url}")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers or {})  # noqa: S310
    if body is not None:
        req.add_header("Content-Type", "application/json")
    ctx = ssl.create_default_context()

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None

    handlers = [urllib.request.HTTPSHandler(context=ctx)]
    if not follow_redirects:
        handlers.append(NoRedirect())
    opener = urllib.request.build_opener(*handlers)
    try:
        with opener.open(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as e:
        return 0, {}, f"network error: {e}"


def wix_api(path: str, body: dict, site_id: str | None) -> tuple[int, dict | str]:
    headers = {"Authorization": os.environ["WIX_API_KEY"]}
    if site_id:
        headers["wix-site-id"] = site_id
    if os.environ.get("WIX_ACCOUNT_ID"):
        headers["wix-account-id"] = os.environ["WIX_ACCOUNT_ID"]
    status, _, text = http(API_BASE + path, body=body, headers=headers)
    try:
        return status, json.loads(text)
    except json.JSONDecodeError:
        return status, text[:500]


def discover_site_id() -> str | None:
    if os.environ.get("WIX_SITE_ID"):
        return os.environ["WIX_SITE_ID"]
    status, data = wix_api("/site-list/v2/sites/query", {"query": {}}, site_id=None)
    if status != 200 or not isinstance(data, dict):
        add("UNVERIFIED", "API access",
            f"Site discovery failed (HTTP {status}): {json.dumps(data)[:300]}. "
            "Set WIX_SITE_ID (Wix dashboard URL contains it) and/or WIX_ACCOUNT_ID.")
        return None
    sites = data.get("sites", [])
    for s in sites:
        blob = json.dumps(s).lower()
        if APEX_HOST in blob:
            return s.get("id")
    if len(sites) == 1:
        return sites[0].get("id")
    add("UNVERIFIED", "API access",
        f"Could not identify the {SITE_HOST} site among {len(sites)} sites; set WIX_SITE_ID.")
    return None


def audit_collections(site_id: str) -> None:
    status, data = wix_api("/wix-data/v2/collections/query", {}, site_id)
    if status != 200 or not isinstance(data, dict):
        add("UNVERIFIED", "CMS",
            f"Collections query failed (HTTP {status}): {json.dumps(data)[:300]}")
        return
    cols = data.get("collections", [])
    names = {c.get("id", ""): c for c in cols}
    system_prefixes = ("Members", "Marketing", "Stores", "Bookings")
    user_cols = [c for c in names if not c.startswith(system_prefixes)]
    add("INFO", "CMS", f"Collections found: {sorted(user_cols) or 'none'}")
    lower = {n.lower().replace("_", "").replace("-", ""): n for n in names}
    for expected in EXPECTED_COLLECTIONS:
        if expected.lower() not in lower:
            add("GAP", "CMS",
                f"Proposed collection `{expected}` not present (build plan §CMS/content collections).")
    # Maturity labels inside any Systems-like collection.
    for key, actual in lower.items():
        if "system" not in key:
            continue
        query = {"dataCollectionId": actual, "query": {"paging": {"limit": 100}}}
        s2, items = wix_api("/wix-data/v2/items/query", query, site_id)
        if s2 != 200 or not isinstance(items, dict):
            add("UNVERIFIED", "CMS", f"Could not read items of `{actual}` (HTTP {s2}).")
            continue
        for item in items.get("dataItems", []):
            fields = item.get("data", {})
            label = str(fields.get("maturity") or fields.get("status") or "").strip()
            title = fields.get("title") or fields.get("name") or item.get("id")
            if not label:
                add("GAP", "Maturity",
                    f"`{actual}` item '{title}' has no maturity/status field.")
            elif label.lower() not in ALLOWED_MATURITY:
                add("GAP", "Maturity",
                    f"`{actual}` item '{title}' has label '{label}' outside the approved "
                    "vocabulary (Incubator/Experimental/Alpha/Beta/Stable/Deprecated/Archived/Planned).")


def fetch_sitemap() -> tuple[list[str], bool]:
    urls: list[str] = []
    ok = True

    def pull(url: str, depth: int = 0) -> None:
        nonlocal ok
        if depth > 2:
            return
        status, _, text = http(url)
        if status != 200:
            ok = False
            add("UNVERIFIED", "Structure", f"Could not fetch {url} (HTTP {status}).")
            return
        locs = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", text)
        for loc in locs:
            if loc.endswith(".xml"):
                pull(loc, depth + 1)
            else:
                urls.append(loc)

    pull(f"https://{SITE_HOST}/sitemap.xml")
    return sorted(set(urls)), ok


class TextAndStyle(HTMLParser):
    """Collects visible text, inline colors, font families, and href targets."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text: list[str] = []
        self.hrefs: list[str] = []
        self.css: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("script",):
            self._skip += 1
        if tag == "style":
            self._skip += 1
            self._in_style = True
        if "style" in d:
            self.css.append(d["style"])
        if tag == "a" and d.get("href"):
            self.hrefs.append(d["href"])

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip:
            if getattr(self, "_in_style", False):
                self.css.append(data)
            return
        if data.strip():
            self.text.append(data.strip())


def luminance(hexcolor: str) -> float:
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return 0.5
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def audit_page(url: str, is_home: bool) -> None:
    status, _, html = http(url)
    if status == 0:
        add("UNVERIFIED", "Structure", f"{url} unreachable: {html}")
        return
    if status != 200:
        add("GAP", "Structure", f"{url} returned HTTP {status}.")
        return
    parser = TextAndStyle()
    parser.feed(html)
    text = " ".join(parser.text)
    lower = text.lower()
    css = " ".join(parser.css) + " " + " ".join(
        re.findall(r'background(?:-color)?\s*:\s*[^;"}]+', html))

    for term in UNTRUTHFUL_TERMS:
        if term in lower:
            add("GAP", "Truthfulness", f"{url}: contains '{term}' — verify against brand voice "
                "(no implied staff scale, accreditation, or production maturity).")

    if is_home:
        for required in REQUIRED_HOME_TEXT:
            if required.lower() not in lower:
                add("GAP", "Homepage", f"Required hero/founder text missing: \"{required}\"")
        for link in REQUIRED_SITE_LINKS:
            if not any(link in h.lower() for h in parser.hrefs) and link not in lower:
                add("GAP", "Content", f"No visible '{link}' link/text found on homepage "
                    "(required before initial publication).")
        bgs = re.findall(r"background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})", css)
        light = [b for b in bgs if luminance(b) > 0.6]
        dark = [b for b in bgs if luminance(b) < 0.25]
        add("INFO", "Brand",
            f"Homepage background colors observed: {sorted(set(bgs)) or 'none inline'} "
            f"(dark={len(dark)}, light={len(light)})")
        if bgs and len(light) > len(dark):
            add("GAP", "Brand", "Homepage backgrounds are predominantly light — spec requires "
                "near-black canvas with warm cream foreground (cream-on-black).")
        fonts = sorted(set(re.findall(r"font-family\s*:\s*([^;\"}]+)", html.lower())))[:10]
        add("INFO", "Brand", f"Font families observed: {fonts or 'none found in inline CSS'}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="write markdown report to this path")
    ap.add_argument("--max-pages", type=int, default=30)
    args = ap.parse_args()

    if not os.environ.get("WIX_API_KEY"):
        print("WIX_API_KEY is not set; CMS checks will be skipped.", file=sys.stderr)
    else:
        site_id = discover_site_id()
        if site_id:
            add("INFO", "API access", f"Auditing Wix site id {site_id} (read-only).")
            audit_collections(site_id)

    # Apex redirect (handoff checklist §Domain).
    status, headers, _ = http(f"https://{APEX_HOST}/", follow_redirects=False)
    loc = headers.get("Location", "")
    if status in (301, 308) and SITE_HOST in loc:
        add("PASS", "Domain", f"Apex redirects permanently to {loc}")
    elif status == 0:
        add("UNVERIFIED", "Domain", f"Apex https://{APEX_HOST}/ unreachable (network error).")
    else:
        add("GAP", "Domain", f"Apex https://{APEX_HOST}/ does not 301 to www "
            f"(got HTTP {status}, Location: {loc or 'none'}).")

    urls, sitemap_ok = fetch_sitemap()
    if sitemap_ok:
        add("INFO", "Structure", f"Sitemap pages ({len(urls)}): " + ", ".join(urls))
        paths = " ".join(urls).lower()
        for section, slugs in EXPECTED_TOP_SECTIONS.items():
            if not any(s in paths for s in slugs):
                add("GAP", "Structure",
                    f"Approved page-tree section '{section}' not found in sitemap.")
        for system in EXPECTED_SYSTEM_PAGES:
            if system not in paths:
                add("GAP", "Structure",
                    f"System page or planned-state entry for '{system}' not found in sitemap.")

    home = f"https://{SITE_HOST}/"
    audit_page(home, is_home=True)
    for url in [u for u in urls if u.rstrip("/") != home.rstrip("/")][: args.max_pages]:
        audit_page(url, is_home=False)

    order = {"GAP": 0, "UNVERIFIED": 1, "PASS": 2, "INFO": 3}
    findings.sort(key=lambda f: order.get(f[0], 9))
    lines = ["# Wix site audit — punch list", "",
             f"Site: https://{SITE_HOST}/  |  read-only audit", ""]
    for severity, area, message in findings:
        lines.append(f"- **{severity}** [{area}] {message}")
    report = "\n".join(lines) + "\n"
    print(report)
    if args.out:
        with open(args.out, "w") as f:
            f.write(report)
    return 1 if any(s == "GAP" for s, _, _ in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
