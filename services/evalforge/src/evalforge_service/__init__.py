"""EvalForge package exports."""

from .evaluator import EvalForge, EvaluationReport
from .graders import CaseExpectation, CaseGrade, grade_case
from .observed import ObservedEvent, ObservedRun
from .permission_suite import run_permission_trajectory_suite
from .replay import (
    capture_reference_replays,
    sign_manifest_body,
    verify_manifest_signature,
    verify_replay_bundle,
    write_replay_bundle,
)
from .report import build_permission_trajectory_report

__all__ = [
    "CaseExpectation",
    "CaseGrade",
    "EvalForge",
    "EvaluationReport",
    "ObservedEvent",
    "ObservedRun",
    "build_permission_trajectory_report",
    "capture_reference_replays",
    "grade_case",
    "run_permission_trajectory_suite",
    "sign_manifest_body",
    "verify_manifest_signature",
    "verify_replay_bundle",
    "write_replay_bundle",
]

__version__ = "0.3.0"
