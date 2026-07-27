"""Approved-root file tools with traversal protection and exact write approval."""

from __future__ import annotations

import difflib
import os
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

from drl_ai_core import canonical_digest


@dataclass(frozen=True, slots=True)
class WriteProposal:
    relative_path: str
    content: str
    digest: str
    diff: str


class SandboxedWorkspace:
    """Operate only inside one explicitly approved canonical root."""

    def __init__(self, root: Path, *, max_read_bytes: int = 1_000_000) -> None:
        self.root = root.resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("Approved workspace root must be a directory")
        self.max_read_bytes = max_read_bytes

    def _resolve(self, relative_path: str, *, must_exist: bool) -> Path:
        requested = Path(relative_path)
        if requested.is_absolute() or ".." in requested.parts:
            raise PermissionError("Path escapes the approved workspace")
        candidate = self.root / requested
        current = self.root
        for part in requested.parts:
            current = current / part
            if current.is_symlink():
                raise PermissionError("Symbolic links are not approved workspace resources")
        resolved = candidate.resolve(strict=must_exist)
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise PermissionError("Path escapes the approved workspace") from exc
        return resolved

    def list_files(self, relative_directory: str = ".", *, limit: int = 200) -> list[str]:
        if limit <= 0 or limit > 1000:
            raise ValueError("File-list limit must be between 1 and 1000")
        directory = self._resolve(relative_directory, must_exist=True)
        if not directory.is_dir():
            raise ValueError("Requested path is not a directory")
        files: list[str] = []
        for path in sorted(directory.rglob("*")):
            if path.is_symlink() or not path.is_file():
                continue
            resolved = path.resolve(strict=True)
            try:
                relative = resolved.relative_to(self.root)
            except ValueError:
                continue
            files.append(relative.as_posix())
            if len(files) >= limit:
                break
        return files

    def read_text(self, relative_path: str) -> str:
        path = self._resolve(relative_path, must_exist=True)
        if not path.is_file():
            raise ValueError("Only ordinary files may be read")
        if path.stat().st_size > self.max_read_bytes:
            raise ValueError("File exceeds the approved read limit")
        data = path.read_bytes()
        if b"\x00" in data:
            raise ValueError("Binary files require a specialized tool")
        return data.decode("utf-8")

    def propose_write(self, relative_path: str, content: str) -> WriteProposal:
        path = self._resolve(relative_path, must_exist=False)
        previous = ""
        if path.exists():
            previous = self.read_text(relative_path)
        diff = "".join(
            difflib.unified_diff(
                previous.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile=f"a/{relative_path}",
                tofile=f"b/{relative_path}",
            )
        )
        digest = canonical_digest(
            {
                "operation": "write_text",
                "root": str(self.root),
                "relative_path": relative_path,
                "content": content,
            }
        )
        return WriteProposal(relative_path, content, digest, diff)

    def apply_write(self, proposal: WriteProposal, *, approval_digest: str) -> Path:
        if proposal.digest != approval_digest:
            raise PermissionError("Approval is not bound to this exact write")
        expected = self.propose_write(proposal.relative_path, proposal.content)
        if expected.digest != proposal.digest or expected.diff != proposal.diff:
            raise PermissionError("Workspace changed after approval; request a new approval")
        destination = self._resolve(proposal.relative_path, must_exist=False)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=destination.parent,
            delete=False,
        ) as handle:
            handle.write(proposal.content)
            temporary = Path(handle.name)
        os.replace(temporary, destination)
        return destination
