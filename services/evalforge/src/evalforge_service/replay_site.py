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
                f"refusing to render unverified bundle {bundle_dir.name}: " + "; ".join(problems)
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
  color-scheme: dark;
  --canvas: #090a09;
  --panel: #10120f;
  --panel-raised: #151812;
  --ink: #f0ead8;
  --muted: #aaa594;
  --faint: #777569;
  --line: #303229;
  --line-strong: #4a4c3d;
  --accent: #d6b46a;
  --ok: #91bd7a;
  --bad: #df765e;
  --mono: "IBM Plex Mono", "Cascadia Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --sans: "IBM Plex Sans", Inter, system-ui, -apple-system, sans-serif;
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background:
    linear-gradient(90deg, rgb(214 180 106 / 4%) 1px, transparent 1px) 0 0 / 5rem 5rem,
    linear-gradient(rgb(214 180 106 / 3%) 1px, transparent 1px) 0 0 / 5rem 5rem,
    var(--canvas);
  color: var(--ink);
  font-family: var(--sans);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-underline-offset: .2em; text-decoration-thickness: 1px; }
a:hover { color: var(--ink); }
a:focus-visible, [tabindex="0"]:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
}
.skip-link {
  position: absolute; left: 1rem; top: -5rem; z-index: 10;
  padding: .7rem 1rem; background: var(--ink); color: var(--canvas);
  font-family: var(--mono); font-size: .8rem;
}
.skip-link:focus { top: 1rem; }
.shell { width: min(100% - 2rem, 74rem); margin: 0 auto; }
.site-header {
  border-bottom: 1px solid var(--line);
  background: rgb(9 10 9 / 92%);
}
.masthead {
  min-height: 5.4rem; display: flex; align-items: center; justify-content: space-between;
  gap: 1.5rem; padding: 1rem 0;
}
.brand { display: flex; align-items: center; gap: .9rem; color: var(--ink); text-decoration: none; }
.brand-mark {
  display: grid; place-items: center; width: 2.4rem; height: 2.4rem;
  border: 1px solid var(--line-strong); font: 650 .72rem/1 var(--mono);
  letter-spacing: .08em; color: var(--accent);
}
.brand-name { display: block; font-family: var(--serif); font-size: 1rem; letter-spacing: .015em; }
.brand-sub { display: block; margin-top: .12rem; color: var(--faint); font: .68rem/1.2 var(--mono);
             letter-spacing: .09em; text-transform: uppercase; }
.site-nav { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: .35rem 1.1rem; }
.site-nav a { color: var(--muted); font: .72rem/1.4 var(--mono); letter-spacing: .05em;
              text-decoration: none; text-transform: uppercase; }
.site-nav a:hover { color: var(--accent); }
main { padding: clamp(3rem, 7vw, 6rem) 0 5rem; }
.hero { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(15rem, .7fr);
        gap: clamp(2rem, 6vw, 5rem); align-items: end; }
.eyebrow { margin: 0 0 1rem; color: var(--accent); font: .72rem/1.4 var(--mono);
           letter-spacing: .12em; text-transform: uppercase; }
h1, h2, h3 { color: var(--ink); }
h1 { max-width: 13ch; margin: 0; font: 500 clamp(2.7rem, 8vw, 6.6rem)/.92 var(--serif);
     letter-spacing: -.045em; }
h2 { margin: 4.5rem 0 1rem; padding-top: 1rem; border-top: 1px solid var(--line);
     font: 500 clamp(1.45rem, 3vw, 2.15rem)/1.1 var(--serif); letter-spacing: -.02em; }
h3 { margin: 0; font: 550 1.15rem/1.25 var(--serif); }
.lede { max-width: 48rem; color: var(--muted); font-size: clamp(1rem, 2vw, 1.18rem); }
.hero .lede { margin: 1.5rem 0 0; }
.hero-aside { border-left: 1px solid var(--line); padding-left: 1.25rem; }
.readout { margin: 0; display: grid; gap: 1rem; }
.readout div { display: grid; grid-template-columns: 1fr auto; gap: 1rem; align-items: baseline; }
.readout dt { color: var(--faint); font: .68rem/1.4 var(--mono); letter-spacing: .09em;
              text-transform: uppercase; }
.readout dd { margin: 0; color: var(--ink); font: .8rem/1.4 var(--mono); text-align: right; }
.readout .ok { color: var(--ok); }
.readout .bad { color: var(--bad); }
.meta { display: flex; flex-wrap: wrap; gap: .5rem; margin: 1.25rem 0 0; padding: 0;
        list-style: none; }
.meta li { border: 1px solid var(--line); padding: .34rem .6rem; color: var(--muted);
           font: .7rem/1.25 var(--mono); letter-spacing: .035em; text-transform: uppercase; }
.meta li.tag-ok { color: var(--ok); border-color: rgb(145 189 122 / 48%); }
.meta li.tag-bad { color: var(--bad); border-color: rgb(223 118 94 / 52%); }
.meta li.tag-accent { color: var(--accent); border-color: rgb(214 180 106 / 45%); }
.note { margin: 2rem 0; padding: 1rem 1.1rem; border: 1px solid var(--line);
        border-left: 3px solid var(--accent); background: var(--panel); color: var(--muted);
        font-size: .92rem; }
.note strong { color: var(--ink); }
.note.is-danger { border-left-color: var(--bad); }
.cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem;
         margin-top: 1.5rem; }
.card { position: relative; display: flex; flex-direction: column; min-height: 19rem;
        padding: 1.35rem; border: 1px solid var(--line); background: var(--panel); }
.card::before { content: attr(data-index); position: absolute; top: 1.15rem; right: 1.2rem;
                color: var(--faint); font: .68rem/1 var(--mono); }
.card-kicker { margin: 0 0 .65rem; color: var(--faint); font: .68rem/1.4 var(--mono);
               letter-spacing: .1em; text-transform: uppercase; }
.card p { color: var(--muted); font-size: .92rem; }
.card .meta { margin-top: auto; }
.card-action { margin: 1rem 0 0; font: .76rem/1.4 var(--mono); letter-spacing: .04em;
               text-transform: uppercase; }
.card-action a { display: inline-block; }
.section-intro { max-width: 48rem; color: var(--muted); }
ol.trace { margin: 0; padding: 0; list-style: none; counter-reset: trace;
           border-top: 1px solid var(--line); }
ol.trace li { counter-increment: trace; display: grid; grid-template-columns: 2.5rem 7rem 1fr;
              gap: 1rem; padding: .8rem 0; border-bottom: 1px solid var(--line); }
ol.trace li::before { content: counter(trace, decimal-leading-zero); padding-top: .1rem;
                      color: var(--faint); font: .68rem/1.5 var(--mono); }
.state { padding-top: .1rem; color: var(--faint); font: .68rem/1.5 var(--mono);
         letter-spacing: .06em; text-transform: uppercase; }
.event { color: var(--accent); font: .76rem/1.5 var(--mono); letter-spacing: .02em; }
.msg { margin-top: .12rem; font-size: .92rem; }
li.is-failure { background: linear-gradient(90deg, rgb(223 118 94 / 10%), transparent 62%); }
li.is-failure .event, li.is-failure .msg { color: var(--bad); }
li.is-tool { background-color: rgb(21 24 18 / 55%); }
.table-region { overflow-x: auto; border: 1px solid var(--line); background: var(--panel); }
.table-region:focus-visible { outline-offset: -3px; }
table { width: 100%; min-width: 42rem; border-collapse: collapse; font-size: .88rem; }
caption { padding: .75rem .85rem; border-bottom: 1px solid var(--line); color: var(--muted);
          font: .7rem/1.4 var(--mono); letter-spacing: .07em; text-align: left;
          text-transform: uppercase; }
th, td { padding: .7rem .8rem; border-bottom: 1px solid var(--line); text-align: left;
         vertical-align: top; }
tr:last-child th, tr:last-child td { border-bottom: 0; }
th { color: var(--faint); font: 500 .68rem/1.4 var(--mono); letter-spacing: .06em;
     text-transform: uppercase; }
tbody th { color: var(--muted); }
code, .digest { color: var(--muted); font: .76rem/1.5 var(--mono); word-break: break-word; }
ul.plain { max-width: 54rem; padding-left: 1.2rem; color: var(--muted); font-size: .92rem; }
ul.plain li + li { margin-top: .55rem; }
.actions { display: flex; flex-wrap: wrap; gap: .65rem; margin-top: 2rem; }
.button { display: inline-flex; align-items: center; min-height: 2.8rem; padding: .65rem .9rem;
          border: 1px solid var(--line-strong); color: var(--ink); font: .72rem/1.2 var(--mono);
          letter-spacing: .05em; text-decoration: none; text-transform: uppercase; }
.button.primary { border-color: var(--accent); background: var(--accent); color: var(--canvas); }
.button:hover { border-color: var(--ink); color: var(--accent); }
.button.primary:hover { background: var(--ink); color: var(--canvas); }
.site-footer { padding: 1.5rem 0 3rem; border-top: 1px solid var(--line); color: var(--faint);
               font: .7rem/1.6 var(--mono); }
.site-footer-grid { display: grid; grid-template-columns: 1fr auto; gap: 2rem; }
.site-footer p { margin: 0 0 .45rem; }
.site-footer a { color: var(--muted); }
@media (prefers-reduced-motion: no-preference) {
  html { scroll-behavior: smooth; }
  .card, .button { transition: border-color .15s ease, background-color .15s ease,
                               color .15s ease; }
  .card:hover { border-color: var(--line-strong); }
}
@media (max-width: 48rem) {
  .masthead { align-items: flex-start; flex-direction: column; }
  .site-nav { justify-content: flex-start; }
  .hero { grid-template-columns: 1fr; }
  .hero-aside { border-left: 0; border-top: 1px solid var(--line); padding: 1.25rem 0 0; }
  .cards { grid-template-columns: 1fr; }
  ol.trace li { grid-template-columns: 2rem 1fr; gap: .65rem; }
  .state { grid-column: 2; }
  ol.trace li > div:last-child { grid-column: 2; }
  .site-footer-grid { grid-template-columns: 1fr; }
}
@media (max-width: 30rem) {
  .shell { width: min(100% - 1.25rem, 74rem); }
  .site-nav { gap: .35rem .8rem; }
  h1 { font-size: clamp(2.45rem, 17vw, 4rem); }
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
        '<meta name="color-scheme" content="dark">\n'
        '<meta name="theme-color" content="#090a09">\n'
        '<meta name="description" content="Inspectable prototype research runs from '
        "DeWitt Research Laboratory, including execution traces, evidence lineage, "
        'limitations, and provenance.">\n'
        f"<title>{_esc(title)}</title>\n"
        f"<style>{_STYLE}</style>\n"
        "</head>\n<body>\n"
        '<a class="skip-link" href="#main">Skip to recorded run content</a>\n'
        '<header class="site-header">\n<div class="shell masthead">\n'
        '<a class="brand" href="index.html" aria-label="DeWitt Research Laboratory '
        'recorded runs home"><span class="brand-mark" aria-hidden="true">DRL</span>'
        '<span><span class="brand-name">DeWitt Research Laboratory</span>'
        '<span class="brand-sub">Recorded runs / Evidence archive</span></span></a>\n'
        '<nav class="site-nav" aria-label="Primary">'
        '<a href="index.html">Runs</a>'
        '<a href="https://www.dewitt-labs.com/research">Research</a>'
        '<a href="https://github.com/chris-dewitt/DeWitt-Research-Lab">Source</a>'
        '<a href="https://www.dewitt-labs.com/about-collaborate">About</a>'
        "</nav>\n</div>\n</header>\n"
        f'<main id="main" class="shell" tabindex="-1">\n{body}\n</main>\n'
        f"{_footer()}\n"
        "</body>\n</html>\n"
    )


def _footer() -> str:
    return (
        '<footer class="site-footer">\n<div class="shell site-footer-grid">\n<div>\n'
        "<p>Christopher Noxon DeWitt · Charlotte, North Carolina · "
        "Independent research · Status: Prototype</p>\n"
        "<p>Independent personal research artifact. UNC-Chapel Hill is identified "
        "for educational context and does not endorse this project.</p>\n"
        "</div>\n<div>\n"
        '<p><a href="https://www.dewitt-labs.com">dewitt-labs.com</a></p>\n'
        '<p><a href="mailto:director@dewitt-labs.com">director@dewitt-labs.com</a></p>\n'
        "</div>\n</div>\n</footer>"
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
            f'<tr><th scope="row">{_esc(name)}</th>'
            f"<td>{_esc(present)}</td>"
            f"<td>{evidence_html}</td>"
            f'<td class="digest">{_esc(_short(digest)) if digest else "—"}</td></tr>'
        )
    return (
        '<div class="table-region" tabindex="0" role="region" '
        'aria-label="Evidence lineage table; scroll horizontally on small screens">'
        "<table>\n<caption>Specialist artifacts linked to this recorded run</caption>\n"
        '<thead><tr><th scope="col">artifact</th><th scope="col">present</th>'
        '<th scope="col">evidence ids</th><th scope="col">digest</th></tr></thead>\n<tbody>\n'
        + "\n".join(rows)
        + "\n</tbody></table></div>"
    )


def render_bundle_page(bundle: ReplayBundle) -> str:
    """Render one replay bundle to a standalone HTML page."""
    state_class = "tag-bad" if bundle.degraded else "tag-ok"
    outcome = "degraded" if bundle.degraded else "completed"
    tool_calls = sum(1 for e in bundle.trace if e.get("event_type") == "tool_started")
    run_label = "Resilience test" if bundle.degraded else "Baseline workflow"

    parts = [
        '<section class="hero" aria-labelledby="run-title"><div>',
        f'<p class="eyebrow">Recorded run / {run_label}</p>',
        f'<h1 id="run-title">{_esc(bundle.name)} replay</h1>',
        '<p class="lede">An inspectable recording of the evidence-to-scenario '
        "workflow. The plan, specialist calls, returned evidence, evaluation, "
        "limitations, and linked digests below come from the verified bundle; "
        "they were not reconstructed for presentation.</p>",
        '<div class="actions"><a class="button" href="index.html">All recorded runs</a>'
        '<a class="button" href="https://github.com/chris-dewitt/DeWitt-Research-Lab/'
        'tree/main/services/evalforge/fixtures/signed_replays">Inspect source bundle</a></div>',
        '</div><aside class="hero-aside" aria-label="Run summary"><dl class="readout">',
        f'<div><dt>Outcome</dt><dd class="{"bad" if bundle.degraded else "ok"}">'
        f"{_esc(outcome)}</dd></div>",
        f"<div><dt>Maturity</dt><dd>{_esc(bundle.maturity)}</dd></div>",
        f"<div><dt>Trace events</dt><dd>{len(bundle.trace)}</dd></div>",
        f"<div><dt>Specialist calls</dt><dd>{tool_calls}</dd></div>",
        f"<div><dt>Evidence items</dt><dd>{len(bundle.evidence_ids)}</dd></div>",
        f"<div><dt>Task</dt><dd>{_esc(bundle.task_id)}</dd></div>",
        "</dl></aside></section>",
        "<ul class='meta' aria-label='Run labels'>",
        f'<li class="{state_class}">{_esc(outcome)}</li>',
        f'<li class="tag-accent">{_esc(bundle.maturity)} maturity</li>',
        "<li>fixture evidence</li><li>static replay</li><li>verified at build</li>",
        "</ul>",
        '<div class="note"><strong>Read this as software evidence, not as live '
        "market analysis.</strong> The inputs are deterministic fixtures, the planner "
        "is rule-based, and the signing key is a disclosed demo key. No production "
        "bank data, public inference service, or trained Atticus weights are represented.</div>",
    ]

    if bundle.degraded:
        failed = bundle.failures
        detail = str(failed[0].get("message", "")).strip() if failed else ""
        if detail and not detail.endswith((".", "!", "?")):
            detail += "."
        detail_html = f"<em>{_esc(detail)}</em> " if detail else ""
        parts.append(
            '<div class="note is-danger"><strong>This run failed partway through and kept '
            "going.</strong> "
            f"{detail_html}The workflow completed in a degraded state rather than "
            "collapsing, and the trace below records exactly where it broke. "
            "This recording is published because a system that only shows its "
            "successes is not evidence of anything.</div>"
        )

    parts += [
        "<h2>Execution trace</h2>",
        "<p class='section-intro'>Read from top to bottom. Tool activity is visually "
        "separated from state transitions; a failed specialist call is marked in text "
        "and color.</p>",
        _timeline(bundle),
        "<h2>Evidence lineage</h2>",
        "<p class='section-intro'>What each specialist contributed, and the digests that "
        "tie the artifacts together.</p>",
        _linked_table(bundle),
    ]

    if bundle.evidence_ids:
        parts += [
            "<h2>Evidence</h2>",
            "<p class='section-intro'>Evidence identifiers carried by the run record.</p>",
            '<ul class="plain">'
            + "".join(f"<li><code>{_esc(e)}</code></li>" for e in bundle.evidence_ids)
            + "</ul>",
        ]

    if bundle.limitations:
        parts += [
            "<h2>Limitations</h2>",
            "<p class='section-intro'>Recorded by the run itself, not added afterwards.</p>",
            '<ul class="plain">'
            + "".join(f"<li>{_esc(x)}</li>" for x in bundle.limitations)
            + "</ul>",
        ]

    manifest = bundle.manifest
    parts += [
        "<h2>Provenance</h2>",
        '<p class="section-intro">Build-time verification binds the display to the '
        "recorded artifacts. It does not establish a production signing identity.</p>",
        '<div class="table-region" tabindex="0" role="region" '
        'aria-label="Run provenance table; scroll horizontally on small screens">'
        "<table><caption>Recorded execution and integrity metadata</caption><tbody>"
        '<tr><th scope="row">code revision</th><td><code>'
        f"{_esc(manifest.get('code_revision', '—'))}</code></td></tr>"
        '<tr><th scope="row">executed at</th><td><code>'
        f"{_esc(manifest.get('executed_at', '—'))}</code></td></tr>"
        f'<tr><th scope="row">configuration</th><td class="digest">'
        f"{_esc(_short(manifest.get('configuration_digest', '—'), 32))}</td></tr>"
        '<tr><th scope="row">signature</th><td>verified at build time</td></tr>'
        "</tbody></table></div>",
        '<div class="note">The manifest signature and every artifact digest were '
        "verified before this page was generated; an unverified bundle is not "
        "rendered at all. The signing key is a <strong>demo key</strong>, not a "
        "production signing identity — treat the signature as structural "
        "integrity, not as an attestation of trust.</div>",
        '<div class="actions"><a class="button primary" href="index.html">Compare both runs</a>'
        '<a class="button" href="https://www.dewitt-labs.com/research">Research context</a>'
        '<a class="button" href="https://github.com/chris-dewitt/DeWitt-Research-Lab">'
        "Repository</a></div>",
    ]
    return _page(f"{bundle.name} replay — DeWitt Research Laboratory", "\n".join(parts))


def render_index(bundles: list[ReplayBundle]) -> str:
    """Render the replay index page."""
    cards: list[str] = []
    for index, bundle in enumerate(bundles, start=1):
        state_class = "tag-bad" if bundle.degraded else "tag-ok"
        outcome = "degraded" if bundle.degraded else "completed"
        run_type = "Resilience test" if bundle.degraded else "Baseline workflow"
        blurb = (
            "A specialist fails mid-run. The system records the fault, preserves the "
            "partial evidence, and completes with an explicit degraded outcome."
            if bundle.degraded
            else "The full evidence-to-scenario path: planning, specialist routing, "
            "deterministic calculation, evaluation, and a completed record."
        )
        cards.append(
            f'<article class="card" data-index="RUN {index:02d}">'
            f'<p class="card-kicker">{run_type}</p><h3>{_esc(bundle.name)} replay</h3>'
            f"<p>{blurb}</p>"
            f'<ul class="meta"><li class="{state_class}">{_esc(outcome)}</li>'
            f"<li>{len(bundle.trace)} events</li>"
            f"<li>{len(bundle.evidence_ids)} evidence items</li></ul>"
            f'<p class="card-action"><a href="{_esc(bundle.name)}.html">'
            f"Inspect {run_type.lower()} →</a></p></article>"
        )

    degraded_count = sum(1 for bundle in bundles if bundle.degraded)
    total_events = sum(len(bundle.trace) for bundle in bundles)
    body = [
        '<section class="hero" aria-labelledby="archive-title"><div>',
        '<p class="eyebrow">Public evidence archive / Prototype series 01</p>',
        '<h1 id="archive-title">Recorded research runs</h1>',
        '<p class="lede">DeWitt Research Laboratory studies how bounded AI systems '
        "plan research, route work across specialist tools, preserve evidence lineage, "
        "divide authority, and remain inspectable when something fails. These static "
        "recordings expose the execution—not merely the final answer.</p>",
        '<div class="actions"><a class="button primary" href="#runs">Inspect the runs</a>'
        '<a class="button" href="https://github.com/chris-dewitt/DeWitt-Research-Lab">'
        "View source</a></div></div>",
        '<aside class="hero-aside" aria-label="Archive summary"><dl class="readout">',
        f"<div><dt>Published runs</dt><dd>{len(bundles)}</dd></div>",
        f"<div><dt>Trace events</dt><dd>{total_events}</dd></div>",
        f'<div><dt>Degraded records</dt><dd class="{"bad" if degraded_count else "ok"}">'
        f"{degraded_count}</dd></div>",
        "<div><dt>Runtime required</dt><dd>none</dd></div>",
        '<div><dt>Bundle verification</dt><dd class="ok">passed</dd></div>',
        "<div><dt>Maturity</dt><dd>prototype</dd></div>",
        "</dl></aside></section>",
        '<div class="note">Everything here is <strong>prototype</strong> maturity. '
        "These two recordings are signed <strong>fixture</strong> runs: canned "
        "inputs, a rule-based planner, and a demo signing key so the files cannot "
        "be silently swapped. That is integrity checking, not a production "
        "signature, and the numbers are not live market data. Local Qwen or FRED "
        "runs stay on the operator's machine; they are not published here. "
        '<a href="https://www.dewitt-labs.com/research">Read the research context</a>.</div>',
        '<section id="runs" aria-labelledby="runs-title"><h2 id="runs-title">Run index</h2>',
        '<p class="section-intro">Read the completed baseline first, then compare the '
        "degraded recording. The pair shows both the intended workflow and the system's "
        "behavior when one specialist fails.</p>",
        '<div class="cards">' + "".join(cards) + "</div></section>",
        '<section aria-labelledby="inspect-title"><h2 id="inspect-title">What you can inspect</h2>',
        '<ul class="plain"><li>The complete ordered execution trace and every recorded '
        "state transition.</li><li>Specialist calls, returned evidence identifiers, and "
        "artifact digests.</li><li>Limitations emitted by the run itself, including the "
        "fixture-data boundary.</li><li>Build-time bundle verification and the disclosed "
        "limits of the demo signing identity.</li></ul></section>",
        '<div class="actions"><a class="button" href="https://www.dewitt-labs.com/research">'
        'Research</a><a class="button" href="https://github.com/chris-dewitt/'
        "DeWitt-Research-Lab/blob/main/docs/10-research/reports/"
        'TR-2026-001-integrated-workflow.md">TR-2026-001</a>'
        '<a class="button" href="https://github.com/chris-dewitt/DeWitt-Research-Lab">'
        "Repository</a></div>",
    ]
    return _page("Recorded research runs — DeWitt Research Laboratory", "\n".join(body))


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
