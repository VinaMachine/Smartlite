"""ASR service stub.

Nhiệm vụ: Nhận audio chunk, chạy inference theo `model_pack.json`, trả partial
hoặc final transcript.
"""
from __future__ import annotations

import json
from pathlib import Path

MODEL_PACK = Path(__file__).with_name("model_pack.json")


def load_models() -> dict:
    model_cfg = json.loads(MODEL_PACK.read_text(encoding="utf-8"))
    return model_cfg["tiers"]


def main() -> None:
    tiers = load_models()
    print(f"ASR boot với các tier: {', '.join(tiers)}")


if __name__ == "__main__":
    main()
