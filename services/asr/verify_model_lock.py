"""Verify integrity of model artifacts before deployment."""
from __future__ import annotations

import hashlib
from pathlib import Path

LOCK_PATH = Path(__file__).parents[2] / "ops" / "latency_profile.json"


def compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify(path: Path, expected_hash: str) -> bool:
    return compute_sha256(path) == expected_hash


if __name__ == "__main__":  # pragma: no cover - manual check helper
    if not LOCK_PATH.exists():
        raise SystemExit("Latency profile missing; cannot verify lock")
    digest = compute_sha256(LOCK_PATH)
    print(f"sha256={digest}")
