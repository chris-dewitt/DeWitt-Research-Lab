"""Small deterministic security helpers used by multiple components."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

_SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
)


def canonical_digest(value: Any) -> str:
    """Hash JSON-compatible data using a stable canonical representation."""

    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def redact_text(value: str) -> str:
    """Remove common credential patterns from defensive logs and traces."""

    redacted = value
    for pattern in _SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted
