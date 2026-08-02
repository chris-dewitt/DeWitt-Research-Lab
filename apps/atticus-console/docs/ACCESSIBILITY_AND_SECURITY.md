---
document_id: DRL-CON-101
title: "Atticus Console Accessibility and Security"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Atticus Console Accessibility and Security

## Accessibility

- Semantic status and log regions announce meaningful changes without reading every token.
- Focus stays stable as events stream; approval focus is intentional and restored.
- All animation has reduced-motion and static alternatives.
- Cream, black, and status colors pass contrast; color is never the sole signal.
- Monospace is used for code/data, not all body copy.
- Approval details cannot be visually truncated.
- Core actions are keyboard-operable and touch targets meet mobile needs.
- Audio is optional, muted by default, and accompanied by transcripts/captions.

## Security

- Raw model, Markdown, HTML, document, and tool output is untrusted and rendered through typed/sanitized viewers.
- External links display destination and use safe navigation behavior.
- Approval submission includes auth, origin/CSRF protection, run ID, request digest, and optimistic version.
- Clipboard and export warn when content may be sensitive.
- Generic analytics receives event names and performance only, never prompts, responses, evidence, tool arguments, approvals, or local payloads.
- Replay signatures and digests are verified before a “verified” badge appears.
