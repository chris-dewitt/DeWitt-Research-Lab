#!/usr/bin/env python3
"""Prepare the only files admitted to the public replay deployment mirror."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = ROOT / "configs" / "public-artifact-export.yaml"

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_FORBIDDEN_TEXT = {
    "private key marker": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Windows local path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
    "runner workspace path": re.compile(r"/home/runner/work/"),
}


class PublicArtifactError(ValueError):
    """The proposed public export violates its release policy."""


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise PublicArtifactError(f"policy is not a mapping: {path}")
    return data


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_source(site_dir: Path, artifact: dict[str, Any]) -> list[str]:
    if not site_dir.is_dir():
        raise PublicArtifactError(f"site directory does not exist: {site_dir}")

    expected = set(artifact["expected_source_files"])
    if not expected or any(Path(name).name != name for name in expected):
        raise PublicArtifactError("expected_source_files must contain root-level filenames")

    entries = list(site_dir.iterdir())
    if any(path.is_symlink() for path in entries):
        raise PublicArtifactError("symlinks are prohibited in public artifacts")
    if any(path.is_dir() for path in entries):
        raise PublicArtifactError("unexpected directories are prohibited in replay exports")

    actual = {path.name for path in entries if path.is_file()}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise PublicArtifactError(f"allowlist mismatch: missing={missing}, extra={extra}")

    maximum_file_bytes = int(artifact["maximum_file_bytes"])
    maximum_total_bytes = int(artifact["maximum_total_bytes"])
    total = 0
    for name in sorted(expected):
        path = site_dir / name
        size = path.stat().st_size
        if size > maximum_file_bytes:
            raise PublicArtifactError(f"{name} exceeds maximum_file_bytes")
        total += size
        if path.suffix in {".html", ".json", ".md", ".txt"}:
            text = path.read_text(encoding="utf-8")
            for label, pattern in _FORBIDDEN_TEXT.items():
                if pattern.search(text):
                    raise PublicArtifactError(f"{name} contains forbidden {label}")
    if total > maximum_total_bytes:
        raise PublicArtifactError("public artifact exceeds maximum_total_bytes")
    return sorted(expected)


def _read_exception(policy_path: Path, artifact: dict[str, Any]) -> dict[str, Any]:
    exception_path = ROOT / artifact["open_exception"]
    if policy_path != DEFAULT_POLICY:
        exception_path = policy_path.parents[1] / artifact["open_exception"]
    exception = json.loads(exception_path.read_text(encoding="utf-8"))
    if not isinstance(exception, dict):
        raise PublicArtifactError(
            f"open exception must be a JSON object: {exception_path}"
        )
    if exception["artifact_id"] != artifact["artifact_id"]:
        raise PublicArtifactError("open exception does not match the artifact")
    if exception["status"] != "active":
        raise PublicArtifactError("open exception is not active")
    return exception


def prepare_release(
    site_dir: Path,
    output_dir: Path,
    source_revision: str,
    policy_path: Path = DEFAULT_POLICY,
) -> dict[str, Any]:
    """Validate, copy, and describe the public replay release envelope."""
    if not _SHA_RE.fullmatch(source_revision):
        raise PublicArtifactError("source revision must be a full lowercase Git SHA")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise PublicArtifactError(f"output directory must be empty: {output_dir}")

    policy = _load_yaml(policy_path)
    artifact = policy["artifact"]
    admitted = _validate_source(site_dir, artifact)
    exception = _read_exception(policy_path, artifact)

    output_dir.mkdir(parents=True, exist_ok=True)
    for name in admitted:
        shutil.copyfile(site_dir / name, output_dir / name)

    readme = f"""# DeWitt Research Artifacts

This is the public deployment mirror for selected evidence from
[Christopher Noxon DeWitt's academic portfolio]({policy['canonical_portfolio_url']}).

The current artifact is **{artifact['title']}**, labeled **REPLAY** and
**{artifact['lifecycle_state'].upper()}**. It shows sanitized success and degraded
fixture runs; it is not a live model session or a production Atticus service.

This mirror is `public_only` while the preferred modification source remains
private through 2026-09-30. See `release-manifest.json` for the exact source
revision, file hashes, licenses, limitations, and temporary open exception.

Contact: [{policy['contact']}](mailto:{policy['contact']})
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")

    manifest = {
        "schema_version": "1.0.0",
        "artifact_id": artifact["artifact_id"],
        "title": artifact["title"],
        "lifecycle_state": artifact["lifecycle_state"],
        "classification": artifact["classification"],
        "source_repository": "https://github.com/chris-dewitt/DeWitt-Research-Lab",
        "source_revision": source_revision,
        "target_repository": policy["target_repository"],
        "pages_url": policy["pages_url"],
        "build_commands": [
            "uv run python scripts/build_replay_site.py --out site/replays --metadata",
            "uv run python scripts/prepare_public_replay_release.py "
            "--site-dir site/replays --out site/public-replays "
            "--source-revision <sha>",
        ],
        "licenses": {
            "renderer_software": artifact["software_license"],
            "rendered_content": artifact["content_license"],
        },
        "contact": policy["contact"],
        "known_limitations": artifact["known_limitations"],
        "open_exception": exception,
        "files": [
            {
                "path": name,
                "bytes": (output_dir / name).stat().st_size,
                "sha256": _sha256(output_dir / name),
            }
            for name in admitted
        ],
    }
    (output_dir / "release-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    args = parser.parse_args()
    try:
        manifest = prepare_release(
            args.site_dir, args.out, args.source_revision, args.policy
        )
    except (KeyError, OSError, PublicArtifactError, json.JSONDecodeError) as exc:
        print(f"public replay export failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"prepared {len(manifest['files'])} admitted content files for "
        f"{manifest['target_repository']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
