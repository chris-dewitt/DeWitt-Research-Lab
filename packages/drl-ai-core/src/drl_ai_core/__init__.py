"""Shared deterministic utilities for DRL AI components."""

from .bakeoff import BakeoffCandidate, load_bakeoff_register, run_bakeoff_scaffold
from .gateway import ModelGateway
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
from .security import canonical_digest, redact_text
from .structured_output import (
    StructuredOutputError,
    StructuredOutputValidator,
    StructuredParseResult,
    StructuredTraceEvent,
    ValidationIssue,
    contains_injection_marker,
    extract_json_candidate,
    validate_against_schema,
)

__all__ = [
    "BakeoffCandidate",
    "ChatMessage",
    "ClosedWeightRejectedError",
    "CompletionConstraints",
    "MockOpenWeightProvider",
    "ModelGateway",
    "ModelIdentity",
    "ModelProvider",
    "OutputMode",
    "ProviderError",
    "ProviderTimeoutError",
    "ProviderUnavailableError",
    "StructuredModelResponse",
    "StructuredOutputError",
    "StructuredOutputValidator",
    "StructuredParseResult",
    "StructuredTraceEvent",
    "ValidationIssue",
    "canonical_digest",
    "contains_injection_marker",
    "extract_json_candidate",
    "load_bakeoff_register",
    "redact_text",
    "run_bakeoff_scaffold",
    "validate_against_schema",
]

__version__ = "0.4.0"
