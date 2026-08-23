"""Load FedLens documents from the opt-in official feed store."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from .service import FedDocument


def documents_from_store(root: Path) -> list[FedDocument]:
    path = root / "documents.json"
    if not path.is_file():
        raise FileNotFoundError(
            f"no live FedLens store at {path}; run scripts/refresh_public_feeds.py"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list) or len(items) < 2:
        raise ValueError("live FedLens store needs at least two press items")
    documents: list[FedDocument] = []
    for raw in items:
        if not isinstance(raw, dict):
            continue
        documents.append(
            FedDocument(
                str(raw["document_id"]),
                str(raw["title"]),
                date.fromisoformat(str(raw["published_date"])),
                str(raw["text"]),
                str(raw["citation"]),
            )
        )
    return documents
