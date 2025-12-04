"""API Gateway facade.

Module giữ nhiệm vụ tiếp nhận traffic từ client, kiểm tra schema và
fan-out request tới các dịch vụ lõi (ASR, LLM, TTS...).
"""
from __future__ import annotations

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("config.yaml")


def load_config() -> dict:
    """Load gateway config as JSON-ready dict for debugging/logging."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Gateway config not found: {CONFIG_PATH}")
    data = CONFIG_PATH.read_text(encoding="utf-8")
    # YAML parser cố tình không dùng để tránh phụ thuộc; file đủ nhỏ để convert thủ công.
    config = {}
    for line in data.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        config[key.strip()] = value.strip()
    return config


def main() -> None:
    config = load_config()
    print(json.dumps({"service": "gateway", "config": config}, indent=2))


if __name__ == "__main__":  # pragma: no cover - bootstrap helper
    main()
