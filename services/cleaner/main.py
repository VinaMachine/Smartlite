"""Text cleaner service stub."""
from __future__ import annotations

from pathlib import Path

RULES = Path(__file__).with_name("rules.yaml")


def load_rules() -> str:
    return RULES.read_text(encoding="utf-8")


def main() -> None:
    rules = load_rules()
    print("Loaded cleaner rules:\n" + rules)


if __name__ == "__main__":
    main()
