"""Normalized observation types for deterministic trajectory grading."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ObservedEvent:
    """One content-minimized trace event."""

    event_type: str
    state: str
    message: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ObservedRun:
    """Observable outcome of one evaluation case."""

    case_id: str
    slice_id: str
    terminal_state: str
    events: tuple[ObservedEvent, ...]
    evidence_count: int = 0
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def event_types(self) -> tuple[str, ...]:
        return tuple(event.event_type for event in self.events)

    def has_event(self, event_type: str) -> bool:
        return event_type in self.event_types
