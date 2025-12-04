"""Chuyển payload legacy sang schema v1.

Đây chỉ là ví dụ: thực tế bạn sẽ map từng trường và thêm validation.
"""
from __future__ import annotations

from typing import Any, Dict


def transform(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return payload conforming to session_envelope.v1 schema."""
    mapped = {
        "session_id": payload.get("sid") or payload.get("session_id"),
        "device_tier": payload.get("device", "mobile"),
        "language": payload.get("lang", "vi"),
        "residency": payload.get("geo", "vn"),
        "llm_preset": payload.get("preset", "default"),
        "tts_capability": payload.get("tts_capability", {"device_tts_ok": False}),
        "auth_token": payload.get("auth", ""),
        "traceparent": payload.get("traceparent", ""),
    }
    # Drop None để tuân thủ schema.
    return {k: v for k, v in mapped.items() if v is not None}
