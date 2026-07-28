"""Atticus helpers for validating structured planner/tool proposals."""

from __future__ import annotations

from typing import Any

from drl_ai_core import StructuredOutputValidator

TOOL_CALL_PLAN_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["task_id", "steps"],
    "properties": {
        "task_id": {"type": "string", "minLength": 1},
        "steps": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["tool_name", "arguments", "risk_tier"],
                "properties": {
                    "tool_name": {"type": "string", "minLength": 1},
                    "arguments": {"type": "object"},
                    "risk_tier": {"type": "integer", "minimum": 0, "maximum": 4},
                },
            },
        },
    },
}


def build_tool_plan_validator(*, max_repair_attempts: int = 2) -> StructuredOutputValidator:
    """Return a validator for bounded Atticus tool-plan JSON artifacts."""

    return StructuredOutputValidator(
        TOOL_CALL_PLAN_SCHEMA,
        max_repair_attempts=max_repair_attempts,
        reject_injection_markers=True,
    )
