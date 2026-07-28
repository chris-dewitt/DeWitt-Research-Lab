"""User-controlled local capabilities for private Atticus workflows."""

from .approvals import (
    DEFAULT_APPROVAL_TTL_SECONDS,
    MAX_APPROVAL_TTL_SECONDS,
    ApprovedWriteFlow,
    AuditEvent,
    LocalApprovalGrant,
    LocalAuditLog,
)
from .voice import CaptureState, LocalVoiceSession, VoiceTurn
from .workspace import SandboxedWorkspace, TextInspection, WriteProposal

__all__ = [
    "DEFAULT_APPROVAL_TTL_SECONDS",
    "MAX_APPROVAL_TTL_SECONDS",
    "ApprovedWriteFlow",
    "AuditEvent",
    "CaptureState",
    "LocalApprovalGrant",
    "LocalAuditLog",
    "LocalVoiceSession",
    "SandboxedWorkspace",
    "TextInspection",
    "VoiceTurn",
    "WriteProposal",
]

__version__ = "0.4.0"
