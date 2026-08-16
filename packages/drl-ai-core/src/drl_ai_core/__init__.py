"""Shared deterministic utilities for DRL AI components."""

from .bakeoff import BakeoffCandidate, load_bakeoff_register, run_bakeoff_scaffold
from .bakeoff_harness import (
    BakeoffError,
    BakeoffReport,
    BakeoffTask,
    CandidateRun,
    EvidenceGate,
    GraderSpec,
    SelectionDecision,
    TaskResult,
    TaskSuite,
    grade_response,
    load_task_suite,
    run_bakeoff,
    run_candidate,
    select_winner,
    summarise_blockers,
)
from .gateway import ModelGateway
from .http_provider import HttpOpenAICompatibleProvider, strip_reasoning
from .mock_provider import MockOpenWeightProvider
from .providers import (
    ChatMessage,
    ClosedWeightRejectedError,
    CompletionConstraints,
    ModelIdentity,
    ModelProvider,
    OutputMode,
    ProviderError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    StructuredModelResponse,
)
from .scripted_provider import ScriptedProvider
from .security import canonical_digest, redact_text
from .structured_output import (
    StructuredOutputError,
    StructuredOutputValidator,
    StructuredParseResult,
    StructuredTraceEvent,
    ValidationIssue,
    clip_middle,
    contains_injection_marker,
    extract_json_candidate,
    validate_against_schema,
)

__all__ = [
    "BakeoffCandidate",
    "BakeoffError",
    "BakeoffReport",
    "BakeoffTask",
    "CandidateRun",
    "ChatMessage",
    "ClosedWeightRejectedError",
    "CompletionConstraints",
    "EvidenceGate",
    "GraderSpec",
    "HttpOpenAICompatibleProvider",
    "MockOpenWeightProvider",
    "ModelGateway",
    "ModelIdentity",
    "ModelProvider",
    "OutputMode",
    "ProviderError",
    "ProviderTimeoutError",
    "ProviderUnavailableError",
    "ScriptedProvider",
    "SelectionDecision",
    "StructuredModelResponse",
    "StructuredOutputError",
    "StructuredOutputValidator",
    "StructuredParseResult",
    "StructuredTraceEvent",
    "TaskResult",
    "TaskSuite",
    "ValidationIssue",
    "canonical_digest",
    "clip_middle",
    "contains_injection_marker",
    "extract_json_candidate",
    "grade_response",
    "load_bakeoff_register",
    "load_task_suite",
    "redact_text",
    "run_bakeoff",
    "run_bakeoff_scaffold",
    "run_candidate",
    "select_winner",
    "strip_reasoning",
    "summarise_blockers",
    "validate_against_schema",
]

__version__ = "0.4.0"
