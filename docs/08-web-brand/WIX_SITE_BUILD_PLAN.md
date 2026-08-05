---
document_id: DRL-WEB-019
title: "Wix Personal Academic Portfolio Build Plan"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Wix Personal Academic Portfolio Build Plan

## Objective

Turn `www.dewitt-labs.com` into Christopher Noxon DeWitt's simple academic
portfolio. The website explains who he is, what he is studying, what he builds,
and where he hopes to take that work next.

## Page tree

```text
Home       /          identity, education, interests, selected work, direction
Research   /research  reports, methods, experiments, notes
Projects   /projects  selected systems and engineering work
About      /about     background, current study, goals, contact
```

GitHub, source, writing, recorded runs, and open-source details live inside
Research or Projects rather than becoming additional top-level departments.

## Navigation and hero

Header: `Christopher Noxon DeWitt` with Research, Projects, and About.

Hero:

```text
CHRISTOPHER NOXON DEWITT
Academic Portfolio

I am a student in the Master of Applied Data Science program at the University
of North Carolina at Chapel Hill. I engineer complex systems at work and study
them part time, with the goal of moving from data science toward graduate work
in computer science.

[View my research] [Explore my projects]
```

Remove DeWitt Research Workshop/Laboratory from the masthead, hero, navigation,
SEO title, and social description. Remove mission slogans, fake node/status
lines, uptime, institutional disclosures, and Atticus launch language.

## Homepage blocks

1. Hero and brief personal introduction.
2. Research interests.
3. Selected research: `TR-2026-001`.
4. Selected projects.
5. Optional recorded demonstration.
6. Current learning and computer-science direction.
7. Contact/footer.

## Visual treatment

Retain cream on near-black, restrained mono metadata, thin rules, and selected
research-terminal details. Reduce density and make long-form reading comfortable.
The visual system should feel like one technically minded graduate student's
portfolio, not a command center or fictional academic institution.

## Content safeguards

- Say “student in the Master of Applied Data Science program at the University
  of North Carolina at Chapel Hill.”
- Do not imply that independent projects are university research, coursework,
  endorsed work, or faculty-supervised work unless verified.
- Describe professional context generally; never name the employer or expose its
  code, data, customers, methods, or confidential information.
- Label prototypes and recorded demonstrations accurately.
- Atticus is one project. Do not make it the guide to the website or advertise a
  public service that does not exist.

## Redirects

```text
/laboratory, /systems, /open-source, /teaching, /failure-museum, /status -> /projects or /research
/writing -> /research
```

Keep existing individual project URLs if useful.

## Acceptance

- name, degree program, university, and computer-science direction are visible
  in the first viewport;
- Research, Projects, and About are the only primary navigation items;
- `TR-2026-001` and the recorded run are reachable as selected work;
- no public lab/workshop identity, mission slogan, fake institutional chrome,
  employer name, or unverified university relationship remains;
- phone, tablet, desktop, keyboard, screen-reader, contrast, zoom, and reduced
  motion are reviewed;
- all links work and a saved Wix revision provides rollback.

## Manual build sequence

1. Save a Wix revision and capture current desktop/mobile screens.
2. Replace site name, SEO title, header, hero, and footer.
3. Reduce navigation to Research, Projects, and About.
4. Rebuild the homepage in the seven-block order above.
5. Move report/run/failure material into Research and project evidence.
6. Verify university wording and remove employer or institutional implications.
7. Test responsive, accessibility, links, metadata, and rollback.
