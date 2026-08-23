"""Local official-feed store. Generated files are operator-local."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_FEED_ROOT = Path("data/public-feeds")
OBSERVATIONS_NAME = "observations.json"
DOCUMENTS_NAME = "documents.json"
CHANGES_NAME = "changes.json"
STATUS_NAME = "last_refresh.json"


class FeedStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root) if root is not None else DEFAULT_FEED_ROOT
        self.root.mkdir(parents=True, exist_ok=True)

    def write_json(self, name: str, payload: dict[str, Any]) -> Path:
        path = self.root / name
        path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
        return path

    def read_json(self, name: str) -> dict[str, Any]:
        path = self.root / name
        if not path.is_file():
            raise FileNotFoundError(
                f"public feed store missing {name}; run scripts/refresh_public_feeds.py"
            )
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise ValueError(f"{name} must be a JSON object")
        return loaded

    def observations(self) -> list[dict[str, Any]]:
        payload = self.read_json(OBSERVATIONS_NAME)
        items = payload.get("items")
        if not isinstance(items, list):
            raise ValueError("observations.json missing items list")
        return [item for item in items if isinstance(item, dict)]

    def documents(self) -> list[dict[str, Any]]:
        payload = self.read_json(DOCUMENTS_NAME)
        items = payload.get("items")
        if not isinstance(items, list):
            raise ValueError("documents.json missing items list")
        return [item for item in items if isinstance(item, dict)]
