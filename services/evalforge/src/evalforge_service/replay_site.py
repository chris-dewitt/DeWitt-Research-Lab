"""Static replay viewer: render signed replay bundles as a self-contained site.

The workshop's most interesting artifact is not a description of the system, it is
a *recording* of the system running — the plan, the policy decisions, each
specialist call, the evidence it returned, the digests linking those artifacts,
the evaluation verdict, and the limitations. Both a successful run and a degraded
one where a specialist fails mid-workflow.

This module renders those bundles to static HTML. No backend, no inference, no
cloud account: the output is a directory of files that can be served from GitHub
Pages or any static host.

Integrity is load-bearing here. A replay page asserts "this is what happened", so
:func:`load_bundle` runs the bundle through
:func:`~evalforge_service.replay.verify_replay_bundle` first and refuses to render
anything whose manifest signature or artifact digests do not check out. A viewer
that renders unverified recordings is worse than no viewer, because it lends the
appearance of provenance to content that has none.

The fixture bundles are signed with a demo HMAC key, which is disclosed on every
rendered page. Structural integrity is real; the signing identity is not
production, and the pages say so rather than implying a trust level that does not
exist.
"""

from __future__ import annotations

import html
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .replay import verify_replay_bundle

PUBLIC_REPLAY_SITE_URL = "https://chris-dewitt.github.io/DeWitt-Research-Lab/"

__all__ = [
    "PUBLIC_REPLAY_SITE_URL",
    "ReplayBundle",
    "ReplaySiteError",
    "build_site",
    "load_bundle",
    "render_bundle_page",
    "render_index",
]


class ReplaySiteError(RuntimeError):
    """Raised when a bundle cannot be rendered honestly."""


# Event types that represent a specialist doing work, for timeline emphasis.
TOOL_EVENTS = frozenset({"tool_started", "tool_completed", "tool_failed"})
FAILURE_EVENTS = frozenset({"tool_failed"})

STATE_ORDER = ("received", "planning", "executing", "evaluating", "completed", "degraded")


@dataclass(frozen=True, slots=True)
class ReplayBundle:
    """A verified replay bundle, loaded from disk."""

    name: str
    manifest: dict[str, Any]
    trace: tuple[dict[str, Any], ...]
    summary: dict[str, Any]
    linked_workflow: dict[str, Any]
    evaluation: Any

    @property
    def task_id(self) -> str:
        return str(self.summary.get("task_id") or self.linked_workflow.get("task_id") or self.name)

    @property
    def final_state(self) -> str:
        return str(self.trace[-1].get("state", "unknown")) if self.trace else "unknown"

    @property
    def degraded(self) -> bool:
        return self.final_state == "degraded" or any(
            e.get("event_type") in FAILURE_EVENTS for e in self.trace
        )

    @property
    def maturity(self) -> str:
        return str(self.linked_workflow.get("maturity", "unknown"))

    @property
    def limitations(self) -> tuple[str, ...]:
        return tuple(str(x) for x in self.summary.get("limitations", ()))

    @property
    def evidence_ids(self) -> tuple[str, ...]:
        return tuple(str(x) for x in self.summary.get("evidence_ids", ()))

    @property
    def failures(self) -> tuple[dict[str, Any], ...]:
        return tuple(e for e in self.trace if e.get("event_type") in FAILURE_EVENTS)


def _read_json(path: Path) -> Any:
    if not path.exists():
        raise ReplaySiteError(f"bundle is missing {path.name}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReplaySiteError(f"{path.name} is not valid JSON: {exc}") from exc


def load_bundle(bundle_dir: Path, *, verify: bool = True) -> ReplayBundle:
    """Load a replay bundle, refusing to proceed if verification fails.

    ``verify=False`` exists only for tests that need to construct deliberately
    broken bundles. Site builds always verify.
    """
    if not bundle_dir.is_dir():
        raise ReplaySiteError(f"not a bundle directory: {bundle_dir}")
    if verify:
        problems = verify_replay_bundle(bundle_dir)
        if problems:
            raise ReplaySiteError(
                f"refusing to render unverified bundle {bundle_dir.name}: "
                + "; ".join(problems)
            )

    trace = _read_json(bundle_dir / "execution-trace.json")
    if not isinstance(trace, list):
        raise ReplaySiteError("execution-trace.json must be a list of events")

    return ReplayBundle(
        name=bundle_dir.name,
        manifest=_read_json(bundle_dir / "replay-manifest.json"),
        trace=tuple(trace),
        summary=_read_json(bundle_dir / "task-summary.json"),
        linked_workflow=_read_json(bundle_dir / "linked-workflow.json"),
        evaluation=_read_json(bundle_dir / "evaluation-report.json"),
    )


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

_STYLE = """
:root {
  --canvas: #0b0b0c;
  --panel: #141416;
  --ink: #ede6d6;
  --muted: #9a948a;
  --line: #2a2a2e;
  --accent: #e0a94e;
  --ok: #7fb069;
  --bad: #d9694f;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --sans: "IBM Plex Sans", system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0;
  background: var(--canvas); color: var(--ink);
  font-family: var(--sans); line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 62rem; margin: 0 auto; padding: 2rem 1.25rem 5rem; }
a { color: var(--accent); text-underline-offset: 2px; }
a:focus-visible, button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
h1, h2, h3 { line-height: 1.2; font-weight: 600; }
h1 { font-size: clamp(1.5rem, 4vw, 2.1rem); margin: 0 0 .35rem; }
h2 { font-size: 1.15rem; margin: 2.5rem 0 .75rem; border-bottom: 1px solid var(--line);
     padding-bottom: .4rem; }
.kicker { font-family: var(--mono); font-size: .74rem; letter-spacing: .08em;
          text-transform: uppercase; color: var(--muted); margin: 0 0 1.5rem; }
.lede { color: var(--muted); max-width: 44rem; }
.meta { display: flex; flex-wrap: wrap; gap: .5rem; margin: 1rem 0 0; padding: 0;
        list-style: none; }
.meta li { font-family: var(--mono); font-size: .72rem; border: 1px solid var(--line);
           padding: .25rem .55rem; border-radius: 2px; color: var(--muted); }
/* These must outspecify `.meta li`, which sets colour and border on every tag. */
.meta li.tag-ok { color: var(--ok);
                  border-color: color-mix(in srgb, var(--ok) 45%, var(--line)); }
.meta li.tag-bad { color: var(--bad);
                   border-color: color-mix(in srgb, var(--bad) 45%, var(--line)); }
.meta li.tag-accent { color: var(--accent);
                      border-color: color-mix(in srgb, var(--accent) 45%, var(--line)); }
.cards { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
         margin-top: 1.5rem; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 3px;
        padding: 1.1rem 1.15rem; }
.card h3 { margin: 0 0 .4rem; font-size: 1rem; }
.card p { margin: 0 0 .8rem; color: var(--muted); font-size: .9rem; }
ol.trace { list-style: none; margin: 0; padding: 0; }
ol.trace li { display: grid; grid-template-columns: 5.5rem 1fr; gap: 1rem;
              padding: .6rem 0; border-bottom: 1px solid var(--line); }
ol.trace li:last-child { border-bottom: 0; }
.state { font-family: var(--mono); font-size: .7rem; text-transform: uppercase;
         letter-spacing: .06em; color: var(--muted); padding-top: .15rem; }
.event { font-family: var(--mono); font-size: .78rem; color: var(--accent); }
.msg { font-size: .92rem; margin-top: .15rem; }
li.is-failure .event { color: var(--bad); }
li.is-failure .msg { color: var(--bad); }
li.is-tool { background: color-mix(in srgb, var(--panel) 55%, transparent); }
table { width: 100%; border-collapse: collapse; font-size: .88rem; }
th, td { text-align: left; padding: .5rem .6rem; border-bottom: 1px solid var(--line);
         vertical-align: top; }
th { font-family: var(--mono); font-size: .7rem; text-transform: uppercase;
     letter-spacing: .06em; color: var(--muted); font-weight: 500; }
code, .digest { font-family: var(--mono); font-size: .78rem; color: var(--muted);
                word-break: break-all; }
.scroll { overflow-x: auto; }
.note { background: var(--panel); border-left: 2px solid var(--accent);
        padding: .9rem 1.1rem; margin: 1.5rem 0; font-size: .9rem; color: var(--muted); }
.note strong { color: var(--ink); }
ul.plain { padding-left: 1.1rem; color: var(--muted); font-size: .9rem; }
footer { margin-top: 4rem; padding-top: 1.25rem; border-top: 1px solid var(--line);
         font-family: var(--mono); font-size: .72rem; color: var(--muted); }
@media (prefers-reduced-motion: no-preference) {
  .card { transition: border-color .15s ease; }
  .card:hover { border-color: var(--accent); }
}
"""


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _short(digest: str, keep: int = 20) -> str:
    text = str(digest)
    return text if len(text) <= keep else text[:keep] + "…"


def _page(title: str, body: str) -> str:
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{_esc(title)}</title>\n"
        f"<style>{_STYLE}</style>\n"
        "</head>\n<body>\n"
        f'<div class="wrap">\n{body}\n</div>\n'
        "</body>\n</html>\n"
    )


def _footer() -> str:
    return (
        "<footer>\n"
        "<p>Christopher Noxon DeWitt · Charlotte, North Carolina · "
        "Status: Prototype</p>\n"
        "<p>Independent student research artifact. UNC-Chapel Hill is identified "
        "for educational context and does not endorse this project.</p>\n"
        '<p><a href="https://www.dewitt-labs.com">Return to academic portfolio →</a></p>\n'
        "</footer>"
    )


def _timeline(bundle: ReplayBundle) -> str:
    rows: list[str] = []
    for event in bundle.trace:
        event_type = str(event.get("event_type", ""))
        classes = []
        if event_type in TOOL_EVENTS:
            classes.append("is-tool")
        if event_type in FAILURE_EVENTS:
            classes.append("is-failure")
        cls = f' class="{" ".join(classes)}"' if classes else ""
        rows.append(
            f"<li{cls}>"
            f'<div class="state">{_esc(event.get("state", ""))}</div>'
            f"<div>"
            f'<div class="event">{_esc(event_type)}</div>'
            f'<div class="msg">{_esc(event.get("message", ""))}</div>'
            f"</div></li>"
        )
    return '<ol class="trace">\n' + "\n".join(rows) + "\n</ol>"


def _linked_table(bundle: ReplayBundle) -> str:
    links = bundle.linked_workflow.get("links", {})
    if not isinstance(links, dict) or not links:
        return "<p class='lede'>No linked artifacts recorded.</p>"
    rows: list[str] = []
    for name in sorted(links):
        entry = links[name] if isinstance(links[name], dict) else {}
        evidence = entry.get("evidence_ids") or []
        evidence_html = (
            "<br>".join(f"<code>{_esc(e)}</code>" for e in evidence) if evidence else "—"
        )
        digest = entry.get("digest")
        present = "yes" if entry.get("present") else "no"
        rows.append(
            f"<tr><td><strong>{_esc(name)}</strong></td>"
            f"<td>{_esc(present)}</td>"
            f"<td>{evidence_html}</td>"
            f'<td class="digest">{_esc(_short(digest)) if digest else "—"}</td></tr>'
        )
    return (
        '<div class="scroll"><table>\n'
        "<thead><tr><th>artifact</th><th>present</th><th>evidence ids</th>"
        "<th>digest</th></tr></thead>\n<tbody>\n"
        + "\n".join(rows)
        + "\n</tbody></table></div>"
    )


def render_bundle_page(bundle: ReplayBundle) -> str:
    """Render one replay bundle to a standalone HTML page."""
    state_class = "tag-bad" if bundle.degraded else "tag-ok"
    outcome = "degraded" if bundle.degraded else "completed"
    tool_calls = sum(1 for e in bundle.trace if e.get("event_type") == "tool_started")

    parts = [
        '<p class="kicker"><a href="index.html">← all recorded runs</a> · '
        '<a href="https://www.dewitt-labs.com">academic portfolio</a></p>',
        f"<h1>{_esc(bundle.name)} replay</h1>",
        '<p class="lede">A recorded run of the evidence-to-scenario workflow, '
        "replayed from a signed bundle. Every step below is what actually "
        "happened — nothing here is reconstructed for display.</p>",
        "<ul class='meta'>",
        f'<li class="{state_class}">{_esc(outcome)}</li>',
        f'<li class="tag-accent">maturity: {_esc(bundle.maturity)}</li>',
        f"<li>{len(bundle.trace)} events</li>",
        f"<li>{tool_calls} specialist calls</li>",
        f"<li>{len(bundle.evidence_ids)} evidence items</li>",
        f'<li>task {_esc(bundle.task_id)}</li>',
        "</ul>",
    ]

    if bundle.degraded:
        failed = bundle.failures
        detail = str(failed[0].get("message", "")).strip() if failed else ""
        if detail and not detail.endswith((".", "!", "?")):
            detail += "."
        detail_html = f"<em>{_esc(detail)}</em> " if detail else ""
        parts.append(
            '<div class="note"><strong>This run failed partway through and kept going.</strong> '
            f"{detail_html}The workflow completed in a degraded state rather than "
            "collapsing, and the trace below records exactly where it broke. "
            "This recording is published because a system that only shows its "
            "successes is not evidence of anything.</div>"
        )

    parts += [
        "<h2>Execution trace</h2>",
        _timeline(bundle),
        "<h2>Evidence lineage</h2>",
        "<p class='lede'>What each specialist contributed, and the digests that "
        "tie the artifacts together.</p>",
        _linked_table(bundle),
    ]

    if bundle.evidence_ids:
        parts += [
            "<h2>Evidence</h2>",
            '<ul class="plain">'
            + "".join(f"<li><code>{_esc(e)}</code></li>" for e in bundle.evidence_ids)
            + "</ul>",
        ]

    if bundle.limitations:
        parts += [
            "<h2>Limitations</h2>",
            "<p class='lede'>Recorded by the run itself, not added afterwards.</p>",
            '<ul class="plain">'
            + "".join(f"<li>{_esc(x)}</li>" for x in bundle.limitations)
            + "</ul>",
        ]

    manifest = bundle.manifest
    parts += [
        "<h2>Provenance</h2>",
        '<div class="scroll"><table><tbody>'
        "<tr><th>code revision</th><td><code>"
        f'{_esc(manifest.get("code_revision", "—"))}</code></td></tr>'
        "<tr><th>executed at</th><td><code>"
        f'{_esc(manifest.get("executed_at", "—"))}</code></td></tr>'
        f'<tr><th>configuration</th><td class="digest">'
        f'{_esc(_short(manifest.get("configuration_digest", "—"), 32))}</td></tr>'
        f'<tr><th>signature</th><td>verified at build time</td></tr>'
        "</tbody></table></div>",
        '<div class="note">The manifest signature and every artifact digest were '
        "verified before this page was generated; an unverified bundle is not "
        "rendered at all. The signing key is a <strong>demo key</strong>, not a "
        "production signing identity — treat the signature as structural "
        "integrity, not as an attestation of trust.</div>",
        _footer(),
    ]
    return _page(f"{bundle.name} replay — Christopher Noxon DeWitt", "\n".join(parts))


def render_index(bundles: list[ReplayBundle]) -> str:
    """Render the replay index page."""
    cards: list[str] = []
    for bundle in bundles:
        state_class = "tag-bad" if bundle.degraded else "tag-ok"
        outcome = "degraded" if bundle.degraded else "completed"
        blurb = (
            "A specialist fails mid-run and the workflow finishes anyway, in a "
            "degraded state."
            if bundle.degraded
            else "The full evidence-to-scenario workflow, start to finish."
        )
        cards.append(
            f'<div class="card"><h3>{_esc(bundle.name)}</h3>'
            f"<p>{blurb}</p>"
            f'<ul class="meta"><li class="{state_class}">{_esc(outcome)}</li>'
            f"<li>{len(bundle.trace)} events</li></ul>"
            f'<p style="margin-top:.9rem"><a href="{_esc(bundle.name)}.html">'
            "Open the replay →</a></p></div>"
        )

    body = [
        '<p class="kicker">Christopher Noxon DeWitt · Academic Portfolio</p>',
        "<h1>Recorded research runs</h1>",
        '<p class="lede">I built Atticus and EvalForge to study how bounded AI '
        "systems plan research, route work across specialist tools, preserve "
        "evidence lineage, and remain inspectable when something fails. These "
        "signed recordings expose the plan, policy decisions, specialist calls, "
        "returned evidence, evaluation, and linked digests. They replay without "
        "a model, GPU, or API key.</p>",
        '<div class="note">Everything here is <strong>prototype</strong> maturity. '
        "These two recordings are signed <strong>fixture</strong> runs: canned "
        "inputs, a rule-based planner, and a demo signing key so the files cannot "
        "be silently swapped. That is integrity checking, not a production "
        "signature, and the numbers are not live market data. Local Qwen or FRED "
        "runs stay on the operator's machine; they are not published here. The "
        "academic portfolio is "
        '<a href="https://www.dewitt-labs.com">www.dewitt-labs.com</a>.</div>',
        '<div class="cards">' + "".join(cards) + "</div>",
        _footer(),
    ]
    return _page("Recorded research runs — Christopher Noxon DeWitt", "\n".join(body))


def build_site(
    bundles_root: Path,
    output_dir: Path,
    *,
    verify: bool = True,
) -> list[Path]:
    """Render every bundle under ``bundles_root`` into ``output_dir``.

    Returns the paths written. Raises :class:`ReplaySiteError` if no bundle is
    found, so a misconfigured path fails loudly instead of publishing an empty site.
    """
    if not bundles_root.is_dir():
        raise ReplaySiteError(f"bundles root not found: {bundles_root}")

    dirs = sorted(p for p in bundles_root.iterdir() if p.is_dir())
    bundles = [load_bundle(p, verify=verify) for p in dirs]
    # Show the clean run before the degraded one: a reader needs to know what the
    # workflow does before they can read where it broke. Alphabetical order puts
    # "degraded" first, which reverses that.
    bundles.sort(key=lambda b: (b.degraded, b.name))
    if not bundles:
        raise ReplaySiteError(f"no replay bundles found under {bundles_root}")

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    index_path = output_dir / "index.html"
    index_path.write_text(render_index(bundles), encoding="utf-8")
    written.append(index_path)

    for bundle in bundles:
        page = output_dir / f"{bundle.name}.html"
        page.write_text(render_bundle_page(bundle), encoding="utf-8")
        written.append(page)

    return written


def site_metadata(bundles: list[ReplayBundle]) -> dict[str, Any]:
    """Machine-readable summary of what was published."""
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "bundle_count": len(bundles),
        "bundles": [
            {
                "name": b.name,
                "task_id": b.task_id,
                "final_state": b.final_state,
                "degraded": b.degraded,
                "events": len(b.trace),
                "evidence_items": len(b.evidence_ids),
                "maturity": b.maturity,
            }
            for b in bundles
        ],
    }
