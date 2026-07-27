---
document_id: DRL-WEB-003
title: "Design Tokens and Component Inventory"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Design Tokens and Component Inventory

## Token intent

Actual values live in code and are reviewed for contrast. Semantic names:

```text
color.bg.canvas
color.bg.panel
color.bg.paper
color.text.primary
color.text.muted
color.border.quiet
color.border.active
color.signal.info
color.signal.warning
color.signal.danger
color.signal.success
color.system.atticus / atlas / fedlens / balance / eval
```

Typography:

- display/institution: restrained sans or serif;
- body: high-readability sans/serif;
- metadata/code: mono;
- numeric tables: tabular figures.

Spacing, radius, shadow, z-index, motion duration, and chart tokens are centralized. Dark theme is the canonical cream-on-black experience; a high-contrast/light reading mode may be provided for research documents.

## Component inventory

- institutional header/status strip;
- command palette;
- pane manager;
- document viewer with margin metadata;
- system map;
- project status badge;
- research card and citation;
- evidence/claim graph;
- agent trace graph/timeline;
- tool/policy/approval card;
- model identity/cost strip;
- diff viewer;
- scenario controls and result tables;
- EvalForge comparison table;
- replay/live indicator;
- failure record;
- code/CLI block;
- contribution issue card;
- consent/telemetry controls;
- cold-start/degraded state.

Components include keyboard, screen-reader, empty, loading, error, and reduced-motion behavior in Storybook or equivalent component documentation.
