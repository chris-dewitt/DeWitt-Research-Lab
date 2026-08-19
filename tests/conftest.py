"""Make workspace ``src`` packages importable without installation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_ROOTS = (
    "packages/drl-protocol/src",
    "packages/drl-ai-core/src",
    "research/cfi/src",
    "services/atlas/src",
    "services/fedlens/src",
    "services/balancelab-ai/src",
    "services/evalforge/src",
    "services/atticus-control-plane/src",
    "apps/atticus-local-runner/src",
)

for relative in SRC_ROOTS:
    sys.path.insert(0, str(ROOT / relative))
