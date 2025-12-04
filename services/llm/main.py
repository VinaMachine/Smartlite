"""LLM orchestration stub."""
from __future__ import annotations

import json
from pathlib import Path

PRESETS = Path(__file__).with_name("presets.json")


def load_presets() -> dict:
    return json.loads(PRESETS.read_text(encoding="utf-8"))


def main() -> None:
    presets = load_presets()
    print(f"Available presets: {', '.join(presets.keys())}")


if __name__ == "__main__":
    main()
