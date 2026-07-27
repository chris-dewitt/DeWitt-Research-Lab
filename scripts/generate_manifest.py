#!/usr/bin/env python3
"""Generate a deterministic SHA-256 manifest for the DRL foundation package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_NAMES = {"PACKAGE_MANIFEST.json"}
EXCLUDE_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}
entries = []
for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
    rel = path.relative_to(ROOT)
    if path.name in EXCLUDE_NAMES or any(part in EXCLUDE_PARTS for part in rel.parts):
        continue
    data = path.read_bytes()
    entries.append(
        {
            "path": rel.as_posix(),
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    )
manifest = {
    "schema_version": "1.0.0",
    "package": "DeWitt-Research-Lab-Foundation",
    "generated_at": "2026-07-27",
    "algorithm": "sha256",
    "entry_count": len(entries),
    "entries": entries,
}
(ROOT / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(entries)} manifest entries")
