---
document_id: DRL-WEB-023
title: "Wix Remaining Editor Fixes (Director Paste Pack)"
version: 1.1.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-09-19
---


# Wix remaining editor fixes

Paste pack for content the SEO/Redirect APIs cannot change. Apply in the Wix
editor for `www.dewitt-labs.com`, then Publish.

## Already applied via API (2026-09-19)

- `/projects` → `/work` (was wrongly `/research`); `/projects-1` → `/work`.
- Home/About SEO description (no MADS/UNC in meta): *Forecast engineer and
  graduate student. Independent work on complex systems, agents, and evaluation
  — aiming toward further study in computer science.* Research title set to
  `Research | Chris DeWitt`.
- Research + Projects status enrichment (BODY_END custom embed
  `Research/Projects status enrichment`, id `0505c503-cd89-425e-8b35-da977b7cc2b3`,
  revision `2`): hides original thin Wix cards and shows one maturity/status
  panel per page (TR detail + null result; monorepo systems; SIGKILL/Dead Drift).

Nav already uses `/work` for Projects. Canonical public slug remains `/work`
with `/projects` as a redirect alias.

## 1. Home hero (#3, #8)

Keep the thesis line. Add the name above it. One short body paragraph so CTAs
appear earlier on mobile.

```text
Chris DeWitt

I study complex systems by the way they fail.

Forecast engineer. Applied Data Science graduate student, UNC–Chapel Hill.
Preparing for graduate work in computer science. Charlotte, North Carolina.

I work full time as a forecast engineer and am in my final year of the Master of
Applied Data Science program at UNC–Chapel Hill. I spend weekends building agent
platforms, evaluation harnesses, quantitative tools, and experiments that
occasionally fail in interesting ways. Everything here is independent personal
work — source, tests, failures, and runs you can replay.

[ Explore my projects → /work ]
[ Read the research → /research ]
[ Watch a recorded run → https://chris-dewitt.github.io/DeWitt-Research-Lab/ ]
[ Browse the source → https://github.com/chris-dewitt/DeWitt-Research-Lab ]
```

## 2. GitHub URL (#4)

Find `http://www.github.com/chris-dewitt` (any page) and set the link to:

`https://github.com/chris-dewitt`

## 3. Footer (#5)

Site-wide footer / master page:

```text
Everything shown on this website is independent personal work.

Questions, ideas, or interesting failures:
director@dewitt-labs.com   ← mailto:director@dewitt-labs.com

GitHub · Privacy
```

- GitHub → `https://github.com/chris-dewitt`
- Privacy → `/privacy` (new page below)

## 4. Privacy page (new)

Create page slug `/privacy`:

```text
Privacy

This is an independent personal academic portfolio operated by Christopher Noxon
DeWitt. It is not a laboratory, institute, or employer site.

Contact and inquiry mail goes to director@dewitt-labs.com. Do not send secrets,
credentials, or employer-confidential material.

Wix may process ordinary hosting and traffic metadata for the site. Prefer
minimal analytics. Application subdomains and research-trace donation, if any,
are separate purposes and need their own consent.

No employer name, customer data, or private traces belong on this site.
```

## 5. Research page (#6, #7, #9) — mostly live via embed

A status panel is already injected on `/research` (prototype tags, limitations,
report/source/run links, TR-2026-002 null result, “what is not settled”). Prefer
pasting the same facts into Studio text so the page works without the embed;
then the embed can be disabled.

Deduplicate the repeated intro in the editor. Widen the content column. Under each report:

**TR-2026-001 — Local Integrated Evidence-to-Scenario Workflow**

```text
Prototype · working paper · fixture data only.

Read the report:
https://github.com/chris-dewitt/DeWitt-Research-Lab/blob/main/docs/10-research/reports/TR-2026-001-integrated-workflow.md

Source: https://github.com/chris-dewitt/DeWitt-Research-Lab

Watch a recorded run (signed fixtures, not a live Atticus service):
https://chris-dewitt.github.io/DeWitt-Research-Lab/
```

**TR-2026-002 — Evidence-Gated Model Selection**

```text
Prototype · working paper.

Result: no winner. The evidence gate refused to name a core or edge model.
That null result is the report’s empirical claim, not a missing outcome.

Read the report:
https://github.com/chris-dewitt/DeWitt-Research-Lab/blob/main/docs/10-research/reports/TR-2026-002-evidence-gated-model-selection.md

Source: https://github.com/chris-dewitt/DeWitt-Research-Lab
```

## 6. Projects page `/work` (#6) — mostly live via embed

A status panel is already injected on `/work` (monorepo clarification, five
prototype systems, SIGKILL/Dead Drift status). Prefer permanent Studio paste;
then disable the embed.

Keep Research reports off this page. Clarify the monorepo is one project:

```text
DeWitt Research Lab (project)
Prototype / independent research · reliable agentic systems

An experimental monorepo for studying how open-weight models, deterministic
policy, evaluation, and human approval should divide authority. It is a project
inside this portfolio — not the identity of the website.

[ View repository → https://github.com/chris-dewitt/DeWitt-Research-Lab ]
[ Watch a recorded run → https://chris-dewitt.github.io/DeWitt-Research-Lab/ ]
[ Related research → /research ]
```

Keep Null Horizon / Dead Drift (or current weekend builds) as separate cards
with a single primary repository link each.

## Verify after publish

1. `https://www.dewitt-labs.com/projects` lands on Projects (`/work`).
2. Home meta description uses the light graduate-student line (no MADS/UNC).
3. No `http://www.github.com` links remain.
4. Footer shows clickable `director@dewitt-labs.com`, GitHub, Privacy.
5. Research cards link reports + recorded run; TR-2026-002 states no winner.
6. First viewport shows name + CS graduate direction without three long paragraphs before CTAs.
