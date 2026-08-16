#!/usr/bin/env python3
"""Read-only audit of the live Wix site against approved DRL web specs.

Compares www.dewitt-labs.com and its Wix CMS collections against:
- docs/08-web-brand/BRAND_SYSTEM.md (cream-on-black, prohibited motifs, voice,
  prohibited institutional chrome)
- docs/08-web-brand/SITE_COPY.md (RES-016 page tree, identity, copy rules)
- docs/08-web-brand/WIX_EDITOR_HANDOFF_CHECKLIST.md (domain, structure, truthful
  maturity labels)
- docs/09-open-source/OPEN_SOURCE_MATURITY_MODEL.md (allowed maturity vocabulary)

The page tree and homepage text come from RES-016, which replaced the
workshop-first `WIX_SITE_BUILD_PLAN.md` with a personal academic portfolio. The
CMS collection list still follows the build plan: the collections exist and are
provisioned, and emptying them is a separate decision from shrinking the site.

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
from http.client import HTTPException
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

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

# Approved page tree, as slug fragments to look for in the sitemap.
#
# RES-016 replaced the workshop-first build plan with a personal academic
# portfolio, and the page tree shrank with it: Home, Research, Projects, About.
# The eight-section tree and the page-per-system expectation this used to carry
# came from the superseded plan, and scoring against them produced eleven
# findings that pointed away from the approved site rather than toward it.
#
# A page outside this set is a NOTE, not a GAP. The contract says which pages
# must exist, not which must not — but on a portfolio being deliberately kept
# small, an unlisted page is worth a decision.
EXPECTED_TOP_SECTIONS = {
    "Research": ["research"],
    "Projects": ["projects", "project"],
    "About": ["about"],
}

# Required homepage text (RES-016 identity).
#
# The hero no longer carries a lab name or a slogan: leading with either is what
# RES-016 corrected. Only the identity is required here — the degree-programme
# wording is governed by SITE_COPY.md, which an auditor cannot check for
# exactness without asserting one phrasing over another.
REQUIRED_HOME_TEXT = [
    "Christopher Noxon DeWitt",
    "Academic Portfolio",
]

# Required links/content anywhere on the homepage.
#
# Governance, security, and status pages belonged to the institutional site.
# A portfolio needs to say who to contact, where the code is, and what happens
# to visitor data.
REQUIRED_SITE_LINKS = ["github", "privacy", "contact"]

#: A page carrying less than this much visible text is a stub, not a page.
MIN_PAGE_TEXT_CHARS = 400

# Allowed maturity vocabulary (OPEN_SOURCE_MATURITY_MODEL.md) plus truthful
# planned-state wording from the build plan.
ALLOWED_MATURITY = {
    "incubator", "experimental", "alpha", "beta", "stable",
    "deprecated", "archived", "planned", "prototype", "research preview",
}

# Language that implies institutional history, staff scale, or production
# maturity DRL does not have (BRAND_SYSTEM.md voice + handoff checklist).
#
# These must match phrases that ASSERT affiliation or maturity. Bare nouns like
# "university" or "accredited" appear in the required independent-initiative
# disclosure ("Not a government, university, or accredited institution"), so
# matching them alone flags a compliance item as a violation.
UNTRUTHFUL_TERMS = [
    "our team", "our staff", "our scientists", "our engineers",
    "accredited by", "accredited institution of", "in partnership with the university",
    "university of", "government agency", "government-backed", "federally funded",
    "production-ready", "enterprise-grade", "battle-tested",
    "trusted by", "clients include", "award-winning", "industry-leading",
    "world-class", "patented", "99.9%", "uptime guarantee",
]

# Sentences containing these are truthful disclaimers; never flag terms inside them.
DISCLAIMER_MARKERS = [
    "not a government", "independent initiative", "not affiliated",
    "is not a university", "no accreditation",
]

# Authority furniture BRAND_SYSTEM.md prohibits by name: framing that implies an
# organisation or an operations centre behind one person's prototypes.
#
# "laboratory use only" and "non-public release" are classification-style stamps,
# and on a page anyone can load they are also false.
PROHIBITED_CHROME = [
    "specialist research nodes", "research nodes", "systems nominal",
    "mission control", "operations centre", "operations center",
    "uptime", "our systems", "our researchers", "our lab",
    "laboratory use only", "non-public release", "laboratory alpha",
]

#: An operations-centre badge: `NODE: 01 //`, `CORE: I //`, `UNIT: 3 |`.
#:
#: Matched by shape rather than by wording. The first version of this check
#: listed `uptime` literally, and the string it was written for came back as
#: `CORE: I // STATUS: ACTIVE` — same badge, different nouns, invisible to a
#: word list.
OPS_BADGE = re.compile(r"\b(?:CORE|NODE|UNIT|SYSTEM|SECTOR)\s*[:#]\s*[A-Z0-9IVX]{1,4}\b")

#: Report identifiers a site might cite: TR-2026-001, REF-2026-001, LOG-2026-X.
IDENTIFIER = re.compile(r"\b[A-Z]{2,8}[-_]\d{4}[-_][A-Z0-9]{1,8}\b")

#: A citation head: "DeWitt, C. (2026)" or "Noxon, J. & DeWitt, C. (2024)".
#:
#: The surname class allows interior capitals and apostrophes, because the one
#: surname this site is guaranteed to carry is intercapped.
_SURNAME = r"[A-Z][A-Za-z'’-]+"
_INITIALS = r"[A-Z]\.(?:\s*[A-Z]\.)?"
CITATION = re.compile(
    rf"\b{_SURNAME},\s*{_INITIALS}"
    rf"(?:\s*(?:&|and)\s*{_SURNAME},\s*{_INITIALS})?\s*\(\d{{4}}\)"
)

#: Any percentage on the page. Not a violation on its own — a result with a
#: linked source is fine — but a number presented as a finding needs one.
PERCENT_CLAIM = re.compile(r"\b\d{1,3}\.\d%|\b\d{1,3}%")

findings: list[tuple[str, str, str]] = []  # (severity, area, message)


def add(severity: str, area: str, message: str) -> None:
    findings.append((severity, area, message))


def http(url: str, *, body: dict[str, Any] | None = None,
         headers: dict[str, str] | None = None, follow_redirects: bool = True,
         timeout: int = 30) -> tuple[int, dict[str, str], str]:
    """GET (or POST when body given) returning (status, headers, text)."""
    if not url.startswith("https://"):
        raise ValueError(f"refusing non-https URL: {url}")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers or {})  # noqa: S310
    if body is not None:
        req.add_header("Content-Type", "application/json")
    ctx = ssl.create_default_context()

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args: Any, **kwargs: Any) -> None:
            return None

    handlers: list[urllib.request.BaseHandler] = [urllib.request.HTTPSHandler(context=ctx)]
    if not follow_redirects:
        handlers.append(NoRedirect())
    opener = urllib.request.build_opener(*handlers)
    try:
        with opener.open(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError, HTTPException) as e:
        # HTTPException covers truncated chunked responses (IncompleteRead), which
        # are not OSError subclasses and would otherwise abort the whole run.
        return 0, {}, f"network error: {e}"


def wix_api(path: str, body: dict[str, Any], site_id: str | None,
            method: str = "POST") -> tuple[int, dict[str, Any] | str]:
    headers = {"Authorization": os.environ["WIX_API_KEY"]}
    if site_id:
        headers["wix-site-id"] = site_id
    if os.environ.get("WIX_ACCOUNT_ID"):
        headers["wix-account-id"] = os.environ["WIX_ACCOUNT_ID"]
    payload = body if method == "POST" else None
    status, _, text = http(API_BASE + path, body=payload, headers=headers)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return status, text[:500]
    return status, parsed if isinstance(parsed, dict) else text[:500]


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
            sid = s.get("id")
            return sid if isinstance(sid, str) else None
    if len(sites) == 1:
        sid = sites[0].get("id")
        return sid if isinstance(sid, str) else None
    add("UNVERIFIED", "API access",
        f"Could not identify the {SITE_HOST} site among {len(sites)} sites; set WIX_SITE_ID.")
    return None


def audit_collections(site_id: str) -> None:
    # Collections are listed via GET; the /collections/query POST route returns 404.
    status, data = wix_api("/wix-data/v2/collections", {}, site_id, method="GET")
    if status != 200 or not isinstance(data, dict):
        blob = json.dumps(data)
        if "WDE0110" in blob:
            add("UNVERIFIED", "CMS",
                "Wix CMS app is not installed for this site, so no collections exist. "
                "Install it before auditing content collections.")
        else:
            add("UNVERIFIED", "CMS",
                f"Collections query failed (HTTP {status}): {blob[:300]}")
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
                f"Proposed collection `{expected}` not present "
                "(build plan §CMS/content collections).")
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
                    "vocabulary (Incubator/Experimental/Alpha/Beta/Stable/"
                    "Deprecated/Archived/Planned).")


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
        self._in_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = dict(attrs)
        if tag == "script":
            self._skip += 1
        if tag == "style":
            self._skip += 1
            self._in_style = True
        style = d.get("style")
        if style:
            self.css.append(style)
        href = d.get("href")
        if tag == "a" and href:
            self.hrefs.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        if tag == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._skip:
            if self._in_style:
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


def flag_untruthful(text: str) -> list[str]:
    """Return untruthful terms present in `text`, ignoring truthful disclaimers.

    Terms inside a sentence that also carries a disclaimer marker (e.g. "This is an
    independent initiative. Not a government, university, or accredited institution.")
    are compliance content, not violations, and must not be reported.
    """
    hits: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        low = sentence.lower()
        if any(marker in low for marker in DISCLAIMER_MARKERS):
            continue
        hits.extend(term for term in UNTRUTHFUL_TERMS if term in low)
    return sorted(set(hits))


def flag_chrome(text: str) -> list[str]:
    """Return institutional-chrome phrases present in ``text``.

    Separate from :func:`flag_untruthful` because the fix is different. An
    untruthful term is a claim to withdraw; chrome is decoration to delete — the
    site is not lying about an operations centre so much as dressing as one.
    """
    lowered = text.lower()
    return sorted({phrase for phrase in PROHIBITED_CHROME if phrase in lowered})


def known_document_ids(root: Path | None = None) -> frozenset[str]:
    """Every report identifier the repository actually defines.

    Read from front matter and filenames under ``docs/``, so the set is whatever
    exists rather than a list to keep in step by hand. Only the head of each file
    is scanned: an identifier mentioned in passing inside a document is a
    reference, not a declaration, and treating it as one would let a citation
    validate itself.
    """
    base = (root or ROOT) / "docs"
    if not base.is_dir():
        return frozenset()
    found: set[str] = set()
    for path in base.rglob("*.md"):
        found.update(IDENTIFIER.findall(path.name.upper()))
        try:
            head = path.read_text(encoding="utf-8", errors="replace")[:400]
        except OSError:
            continue
        found.update(IDENTIFIER.findall(head.upper()))
    return frozenset(found)


def unknown_identifiers(text: str, known: frozenset[str]) -> list[str]:
    """Return report identifiers on the page that no repository document defines."""
    return sorted(set(IDENTIFIER.findall(text.upper())) - known)


def unsourced_citations(text: str, known: frozenset[str]) -> list[str]:
    """Return citations with no repository document identifier beside them.

    Every publication behind this site is a self-published working paper that
    carries its own document id. A citation naming a journal, a volume, or an
    archive, with no id within reach of it, is citing something that does not
    exist here.
    """
    upper = text.upper()
    out: list[str] = []
    for match in CITATION.finditer(text):
        window = upper[match.start() : match.start() + 240]
        if not any(identifier in window for identifier in known):
            out.append(match.group(0))
    return sorted(set(out))


def lookalike_github_hosts(hrefs: list[str]) -> list[str]:
    """Return link hosts that read as GitHub but are not github.com.

    A hyphen in the wrong place sends a portfolio's source-code link to somebody
    else's domain, and it reads as correct in the editor. This is the one link
    defect worth failing an audit over, because the reader who follows it has no
    way to know it was a typo.
    """
    bad: list[str] = []
    for href in hrefs:
        host = re.sub(r"^[a-z]+://", "", href.strip().lower()).split("/")[0]
        host = host.split("@")[-1].split(":")[0]
        if not host or host.endswith(("github.com", "github.io")):
            continue
        stripped = host.replace("-", "").replace("_", "")
        if "github" in stripped:
            bad.append(host)
    return sorted(set(bad))


def resolve_theme_colors(html: str) -> tuple[str | None, str | None]:
    """Resolve the page canvas and foreground colours from Wix CSS variables.

    Wix paints sections via custom properties rather than literal hex in inline
    style attributes, so reading inline hex alone misreports the palette. Prefer
    the explicit --wst-base-N-color tokens, then fall back to the numbered
    --color_NN palette (color_11 is the section background, color_10 the text).
    """
    def rgb_triplet(name: str) -> str | None:
        m = re.search(rf"--{name}\s*:\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", html)
        if not m:
            return None
        return "#{:02x}{:02x}{:02x}".format(*(int(g) for g in m.groups()))

    def hex_token(name: str) -> str | None:
        m = re.search(rf"--{name}\s*:\s*(#[0-9a-fA-F]{{3,8}})", html)
        return m.group(1) if m else None

    canvas = hex_token("wst-base-1-color") or rgb_triplet("color_11")
    foreground = hex_token("wst-base-2-color") or rgb_triplet("color_10")
    return canvas, foreground


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

    for term in flag_untruthful(text):
        add("GAP", "Truthfulness", f"{url}: contains '{term}' — verify against brand voice "
            "(no implied staff scale, accreditation, or production maturity).")

    for phrase in flag_chrome(text):
        add("GAP", "Voice", f"{url}: contains '{phrase}' — institutional chrome prohibited by "
            "BRAND_SYSTEM.md (no operations-centre framing over one person's prototypes).")

    for badge in sorted(set(OPS_BADGE.findall(text)))[:3]:
        add("GAP", "Voice", f"{url}: carries an operations-centre badge ('{badge}'). "
            "Renaming the nouns does not change what it implies.")

    known = known_document_ids()
    for identifier in unknown_identifiers(text, known)[:5]:
        add("GAP", "Evidence", f"{url}: cites '{identifier}', which no document in this "
            "repository defines. A report reference must resolve to docs/10-research/reports/.")

    for citation in unsourced_citations(text, known)[:5]:
        add("GAP", "Evidence", f"{url}: carries the citation '{citation}…' with no repository "
            "document id beside it. Every publication here is a self-published working paper; "
            "a journal or archive citation is citing something that does not exist.")

    for host in lookalike_github_hosts(parser.hrefs):
        add("GAP", "Links", f"{url}: links to '{host}', which is not GitHub. "
            "Check for a typo in the source-code link.")

    for claim in sorted(set(PERCENT_CLAIM.findall(text)))[:5]:
        add("UNVERIFIED", "Evidence", f"{url}: states '{claim}'. A number presented as a result "
            "needs a linked source; confirm it is reproducible from the repository.")

    if len(text) < MIN_PAGE_TEXT_CHARS:
        add("GAP", "Structure", f"{url} has {len(text)} characters of visible text — it is a "
            "stub. Either give it content or take it out of the navigation.")

    if is_home:
        for required in REQUIRED_HOME_TEXT:
            if required.lower() not in lower:
                add("GAP", "Homepage", f"Required hero/founder text missing: \"{required}\"")
        for link in REQUIRED_SITE_LINKS:
            if not any(link in h.lower() for h in parser.hrefs) and link not in lower:
                add("GAP", "Content", f"No visible '{link}' link/text found on homepage "
                    "(required before initial publication).")
        canvas, fg = resolve_theme_colors(html)
        add("INFO", "Brand",
            f"Resolved theme: canvas={canvas or 'unknown'} foreground={fg or 'unknown'}")
        if canvas and luminance(canvas) > 0.35:
            add("GAP", "Brand",
                f"Page canvas {canvas} is not near-black — spec requires a near-black "
                "canvas with warm cream foreground (cream-on-black).")
        elif canvas and fg and luminance(fg) < 0.6:
            add("GAP", "Brand",
                f"Foreground {fg} is not a warm cream against canvas {canvas}.")
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
    # HTTP/2 lowercases header names, so look the header up case-insensitively.
    loc = next((v for k, v in headers.items() if k.lower() == "location"), "")
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
        # Slugs are hyphenated on the live site (/about-me, /open-source), so
        # normalise both sides before comparing.
        flat = re.sub(r"[-_]", "", " ".join(urls).lower())
        for section, slugs in EXPECTED_TOP_SECTIONS.items():
            if not any(re.sub(r"[-_]", "", s) in flat for s in slugs):
                add("GAP", "Structure",
                    f"Approved page-tree section '{section}' not found in sitemap "
                    "(RES-016: Home, Research, Projects, About).")
        approved = {re.sub(r"[-_]", "", s) for slugs in EXPECTED_TOP_SECTIONS.values()
                    for s in slugs}
        home = f"https://{SITE_HOST}"
        for url in urls:
            slug = re.sub(r"[-_]", "", url.rstrip("/").rsplit("/", 1)[-1].lower())
            if url.rstrip("/") == home.rstrip("/") or not slug:
                continue
            if slug not in approved:
                add("NOTE", "Structure",
                    f"{url} is not in the approved page tree. Keeping the portfolio small "
                    "is deliberate; decide whether this page stays.")

    home = f"https://{SITE_HOST}/"
    audit_page(home, is_home=True)
    for url in [u for u in urls if u.rstrip("/") != home.rstrip("/")][: args.max_pages]:
        audit_page(url, is_home=False)

    order = {s: i for i, s in enumerate(("GAP", "UNVERIFIED", "NOTE", "PASS", "INFO"))}
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
