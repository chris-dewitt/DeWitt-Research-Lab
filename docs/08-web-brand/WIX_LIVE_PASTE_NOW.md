---
document_id: DRL-WEB-025
title: "Wix Live Paste Now (Director — do these in Studio)"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Do this in Wix Studio now

You are editing `www.dewitt-labs.com`. Paste these exactly, then **Publish**.
I am updating embeds/API in parallel (Research/Projects tone, gap, softener).

No Chapel Hill / MADS in public body copy. Keep UNC Charlotte on About.

---

## 1. Home hero (first viewport)

**Find** the hero text block (thesis + subtitle + body). Replace with:

```text
Chris DeWitt

I study complex systems by the way they fail.

Forecast engineer and graduate student. Charlotte, North Carolina.

I work full time as a forecast engineer and study applied data science part
time, with an eye toward further graduate work in computer science. Weekends:
agent platforms, evaluation harnesses, quantitative tools, and experiments
that fail in interesting ways. Everything here is independent personal work —
source, tests, failures, and runs you can replay.
```

**CTAs** (keep / retarget if needed):

- Explore my projects → `/work`
- Read the research → `/research`
- Watch a recorded run → `https://chris-dewitt.github.io/DeWitt-Research-Lab/`
- Browse the source → `https://github.com/chris-dewitt/DeWitt-Research-Lab`

**Layout:** Delete or collapse any empty strip / blank section between the hero
CTAs and “Why complex systems?” (the black void). If it is an empty container,
delete it. If it is min-height on a section, set min-height to auto / 0.

**Optional permanent open-weight block** (below Questions, or replace the
embed later):

```text
Open-weight over opaque company APIs

I prefer open-weight models I can run on hardware I own over closed, hosted
systems from large AI vendors. Weights, licenses, and evaluation evidence should
be inspectable. The software around them is open source.

Safe use, concretely: deterministic policy and human approval bound what a model
may do; an evidence gate can refuse to select a model at all; runs stay local by
default so prompts and tools are not shipped to a third-party cloud; failures are
published rather than smoothed over.

No base model has been selected yet. That refusal is deliberate — preference is
not evidence.
```

---

## 2. GitHub URL (site-wide)

Find any link to `http://www.github.com/chris-dewitt` (or similar) and set it to:

`https://github.com/chris-dewitt`

Profile / social icons too.

---

## 3. Footer (master page / site-wide)

Replace footer copy with:

```text
Everything shown on this website is independent personal work.

Questions, ideas, or interesting failures:
director@dewitt-labs.com
```

Link that email as `mailto:director@dewitt-labs.com`.

Add two text links next to it:

- GitHub → `https://github.com/chris-dewitt`
- Privacy → `/privacy`

---

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

---

## 5. About

**Heading:** change `ABOUT CHRIS` → `About`

**Body** (softened — no Chapel Hill):

```text
I'm Chris DeWitt. I work full time as a forecast engineer and study applied
data science part time, and expect to complete my current master's in May 2027.

I'm also a proud graduate of UNC Charlotte. My time there changed my life and
gave me the confidence to keep learning, building, and asking bigger questions.

This portfolio documents independent personal work — research reports, software,
and recorded runs. It is not coursework, not employer work, and not a laboratory.
```

---

## 6. Research + Projects headings

- Page H1: `Research` / `Projects` (sentence case if you can; all-caps nav is fine)
- Keep nav label **PROJECTS** → `/work` (do not rename the route today)

I am rewriting the injected status panels so Research no longer leads with
“not peer-reviewed / not coursework,” and Projects uses a softer monorepo line.

---

## 7. Publish

Click **Publish**. Hard-refresh the live site. Tell me when that lands and I
will re-verify.
