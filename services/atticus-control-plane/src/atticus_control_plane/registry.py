"""Typed in-process tool registry for local and test execution."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from drl_protocol import EvidenceItem, ToolDefinition


@dataclass(slots=True)
class ToolOutput:
    evidence: list[EvidenceItem] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    message: str = ""


ToolHandler = Callable[[dict[str, Any]], ToolOutput]


@dataclass(frozen=True, slots=True)
class RegisteredTool:
    definition: ToolDefinition
    handler: ToolHandler


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register(self, definition: ToolDefinition, handler: ToolHandler) -> None:
        if definition.name in self._tools:
            raise ValueError(f"Tool {definition.name!r} is already registered")
        self._tools[definition.name] = RegisteredTool(definition, handler)

    def definition(self, name: str) -> ToolDefinition | None:
        tool = self._tools.get(name)
        return tool.definition if tool else None

    def invoke(self, name: str, arguments: dict[str, Any]) -> ToolOutput:
        try:
            tool = self._tools[name]
        except KeyError as exc:
            raise LookupError(f"Tool {name!r} is not registered") from exc
        return tool.handler(dict(arguments))

    def catalog(self) -> tuple[ToolDefinition, ...]:
        return tuple(tool.definition for tool in self._tools.values())
