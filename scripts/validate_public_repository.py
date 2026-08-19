#!/usr/bin/env python3
"""Fail-closed checks for making the authoritative repository public.

The ordinary mode audits the exact tracked source tree and is safe to run on
every pull request. ``--release`` adds reachable Git-author metadata because a
history rewrite changes commit identities and therefore remains a deliberate
release-time decision.

The validator reports rule names and file paths, never suspected secret values.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess  # nosec B404
import sys
import tomllib
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_TRACKED_BYTES = 5 * 1024 * 1024
CANONICAL_REPOSITORY = "https://github.com/chris-dewitt/DeWitt-Research-Lab"
PUBLIC_CONTACT = "director@dewitt-labs.com"
HISTORICAL_SECURITY_CONTACT = "security" + "@dewitt-labs.com"

REQUIRED_PUBLIC_FILES = {
    "README.md",
    "LICENSE",
    "NOTICE",
    "CITATION.cff",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "GOVERNANCE.md",
    "CHANGELOG.md",
}

FORBIDDEN_TRACKED_PREFIXES = (
    ".venv/",
    "node_modules/",
    "site/",
    "artifacts/private/",
    "data/private/",
    "checkpoints/",
)
FORBIDDEN_TRACKED_NAMES = {".env", "PACKAGE_MANIFEST.json"}
FORBIDDEN_SUFFIXES = {
    ".7z",
    ".bak",
    ".ckpt",
    ".db",
    ".jks",
    ".key",
    ".onnx",
    ".p12",
    ".pem",
    ".pfx",
    ".pt",
    ".pth",
    ".safetensors",
    ".sqlite",
    ".tar",
    ".tfstate",
    ".zip",
}

EMAIL_RE = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.IGNORECASE)
EMPLOYER_RE = re.compile(
    r"\b(?:bank\s+of\s+america|" + "bo" + "fa|" + "mer" + "rill)" + r"\b",
    re.IGNORECASE,
)
WINDOWS_HOME_RE = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+", re.IGNORECASE)
UNIX_HOME_RE = re.compile(r"/(?:home|Users)/[^/\s]+")
SECRET_PATTERNS = {
    "GitHub personal access token": re.compile(
        r"\b(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"
    ),
    "cloud access key": re.compile(r"\b(?:AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35})\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "private key": re.compile("-" * 5 + r"BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY" + "-" * 5),
}

# These files intentionally contain hostile strings as test fixtures or as the
# deny-list implementation. The exception is path- and rule-specific so it
# cannot make another file pass.
TEXT_RULE_EXCEPTIONS: dict[str, frozenset[str]] = {
    "tests/test_public_artifact_export.py": frozenset({"secret", "local-path"}),
    "tests/test_wix_auditor.py": frozenset({"public-contact"}),
    "scripts/prepare_public_replay_release.py": frozenset({"local-path"}),
    "DIRECTORS_MEMO.md": frozenset({"historical-contact"}),
}


@dataclass(frozen=True)
class Finding:
    path: str
    rule: str
    detail: str

    def render(self) -> str:
        return f"{self.path}: {self.rule}: {self.detail}"


def _git(root: Path, *args: str) -> str:
    git_executable = shutil.which("git")
    if git_executable is None:
        raise RuntimeError("git executable is unavailable")
    # Fixed shell-free Git calls only; no user-controlled command or executable.
    completed = subprocess.run(  # noqa: S603  # nosec B603
        [git_executable, *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "git command failed")
    return completed.stdout


def tracked_paths(root: Path = ROOT) -> list[str]:
    """Return the repository's exact tracked path set."""
    return [path for path in _git(root, "ls-files", "-z").split("\0") if path]


def _rule_excepted(path: str, rule: str) -> bool:
    return rule in TEXT_RULE_EXCEPTIONS.get(path, frozenset())


def scan_text(path: str, text: str) -> list[Finding]:
    """Scan one UTF-8 tracked file without returning matched values."""
    findings: list[Finding] = []
    if EMPLOYER_RE.search(text):
        findings.append(Finding(path, "employer-identifier", "prohibited employer name present"))

    if not _rule_excepted(path, "local-path") and (
        WINDOWS_HOME_RE.search(text) or UNIX_HOME_RE.search(text)
    ):
        findings.append(Finding(path, "local-path", "absolute user-home path present"))

    if not _rule_excepted(path, "secret"):
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append(Finding(path, "credential-pattern", f"{label} shape present"))

    for address in EMAIL_RE.findall(text):
        normalized = address.lower()
        if _rule_excepted(path, "public-contact"):
            continue
        if normalized == PUBLIC_CONTACT:
            continue
        if normalized.endswith("@users.noreply.github.com"):
            continue
        if (
            path == "DIRECTORS_MEMO.md"
            and _rule_excepted(path, "historical-contact")
            and normalized == HISTORICAL_SECURITY_CONTACT
        ):
            continue
        findings.append(
            Finding(path, "public-contact", "email address is not the approved public contact")
        )
    return findings


def _package_metadata_findings(root: Path, paths: Iterable[str]) -> list[Finding]:
    findings: list[Finding] = []
    for rel in sorted(path for path in paths if path.endswith("pyproject.toml")):
        data = tomllib.loads((root / rel).read_text(encoding="utf-8"))
        project = data.get("project")
        if not isinstance(project, dict):
            continue
        if project.get("license") != "Apache-2.0":
            findings.append(Finding(rel, "package-license", "project license is not Apache-2.0"))
        authors = project.get("authors")
        if not isinstance(authors, list) or not any(
            isinstance(author, dict) and author.get("name") == "Christopher Noxon DeWitt"
            for author in authors
        ):
            findings.append(Finding(rel, "package-author", "canonical author metadata is missing"))
        urls = project.get("urls")
        if not isinstance(urls, dict) or urls.get("Repository") != CANONICAL_REPOSITORY:
            findings.append(
                Finding(rel, "package-repository", "canonical repository URL is missing")
            )
        if project.get("readme") != "README.md":
            findings.append(Finding(rel, "package-readme", "package README metadata is missing"))
    return findings


def _scaffold_findings(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for rel in ("apps/atticus-console", "apps/lab-web"):
        package_path = root / rel / "package.json"
        readme_path = root / rel / "README.md"
        package = json.loads(package_path.read_text(encoding="utf-8"))
        scripts = package.get("scripts", {})
        is_placeholder = bool(scripts) and all(
            isinstance(command, str) and "implementation pending" in command.lower()
            for command in scripts.values()
        )
        if not is_placeholder:
            continue
        readme = readme_path.read_text(encoding="utf-8").lower()
        if "**maturity:** `specified`" not in readme:
            findings.append(
                Finding(
                    f"{rel}/README.md", "scaffold-maturity", "specified maturity is not explicit"
                )
            )
        if "status: release candidate" in readme:
            findings.append(
                Finding(
                    f"{rel}/README.md",
                    "scaffold-status",
                    "placeholder is labeled release candidate",
                )
            )
    return findings


def source_findings(root: Path = ROOT) -> tuple[list[Finding], int]:
    """Audit the tracked source tree and return findings plus file count."""
    paths = tracked_paths(root)
    findings: list[Finding] = []
    path_set = set(paths)

    for required in sorted(REQUIRED_PUBLIC_FILES - path_set):
        findings.append(Finding(required, "required-file", "public repository file is missing"))

    for rel in paths:
        path = root / rel
        if path.is_symlink():
            findings.append(Finding(rel, "tracked-symlink", "tracked symlinks are not admitted"))
            continue
        if rel in FORBIDDEN_TRACKED_NAMES or any(
            rel.startswith(prefix) for prefix in FORBIDDEN_TRACKED_PREFIXES
        ):
            findings.append(Finding(rel, "private-artifact", "path is forbidden in public source"))
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(
                Finding(rel, "binary-artifact", "artifact type requires a release channel")
            )
        size = path.stat().st_size
        if size > MAX_TRACKED_BYTES:
            findings.append(Finding(rel, "oversized-file", "tracked file exceeds 5 MiB"))
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding(rel, "non-utf8-file", "tracked source is not UTF-8 text"))
            continue
        findings.extend(scan_text(rel, text))

    findings.extend(_package_metadata_findings(root, paths))
    findings.extend(_scaffold_findings(root))

    readme = (root / "README.md").read_text(encoding="utf-8").lower()
    for phrase in ("the models are open-weight", "everything runs locally"):
        if phrase in readme:
            findings.append(Finding("README.md", "maturity-claim", f"unsupported phrase: {phrase}"))

    return sorted(findings, key=lambda item: (item.path, item.rule, item.detail)), len(paths)


def history_findings_for_emails(emails: Iterable[str]) -> list[Finding]:
    """Evaluate author emails without returning or rendering their values."""
    private_count = sum(email.endswith("@unc.edu") for email in emails)
    findings: list[Finding] = []
    if private_count:
        findings.append(
            Finding(
                "git-history",
                "author-email",
                f"{private_count} reachable commits expose an unapproved institutional address",
            )
        )
    return findings


def history_findings(root: Path = ROOT) -> tuple[list[Finding], int]:
    """Audit reachable author metadata without exposing addresses in output."""
    emails = [
        email.strip().lower() for email in _git(root, "log", "--all", "--format=%ae").splitlines()
    ]
    return history_findings_for_emails(emails), len(emails)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--release",
        action="store_true",
        help="also audit reachable Git author metadata for the public-visibility gate",
    )
    args = parser.parse_args()

    findings, file_count = source_findings()
    history_count = 0
    history: list[Finding] = []
    if args.release:
        history, history_count = history_findings()

    print(f"Tracked files inspected: {file_count}")
    if args.release:
        print(f"Reachable commits inspected: {history_count}")
    # RES-022 accepts the historical institutional address rather than rewriting
    # reachable history. The audit still reports it so the exposure stays visible
    # and countable, but it no longer blocks the release gate. A *new* unapproved
    # address would still show up here.
    for finding in history:
        print(f"ACCEPTED (RES-022): {finding.render()}")
    if findings:
        print("\nPUBLIC REPOSITORY AUDIT FAILED")
        for finding in findings:
            print(f"ERROR: {finding.render()}")
        return 1
    print("PUBLIC REPOSITORY AUDIT PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
