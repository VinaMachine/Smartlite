"""TTS broker stub."""
from __future__ import annotations

import json
from pathlib import Path

VOICES = Path(__file__).with_name("voices.json")


def list_voices() -> list[str]:
    data = json.loads(VOICES.read_text(encoding="utf-8"))
    return [voice["name"] for voice in data]


def main() -> None:
    voices = list_voices()
    print(f"TTS voices ready: {', '.join(voices)}")


if __name__ == "__main__":
    main()
