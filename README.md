# Smartlite Reference Layout

## 4 — Kiến trúc microservice (giải thích đơn giản)
- Hệ thống được tách nhỏ thành các dịch vụ độc lập: ASR, Cleaner, Formatter, LLM, TTS, Post, Delivery và Gateway đóng vai trò điều phối.
- Mỗi dịch vụ tự đóng gói và triển khai riêng bằng Docker hoặc Kubernetes, nên có thể nâng cấp mà không ảnh hưởng phần còn lại.
- Các dịch vụ giao tiếp qua HTTP/gRPC/WebSocket và MessageBus (Kafka) tùy theo latency và throughput.
- Lợi thế chính: sửa / scale một dịch vụ không tác động toàn bộ hệ thống, phù hợp chiến lược scale theo nhu cầu.

## 5 — Cấu trúc thư mục và file quan trọng
```
/smartlite/
  /cmd/                # entrypoints (docker/k8s wrappers)
  /services/
    /gateway/
      main.py
      config.yaml
      schemas/
      transformers/
    /asr/
      main.py
      model_pack.json
      verify_model_lock.py
    /cleaner/
      main.py
      rules.yaml
    /formatter/
      main.py
    /llm/
      main.py
      presets.json
    /tts/
      main.py
      voices.json
    /post/
      main.py
    /delivery/
      main.py
  /ops/
    latency_profile.json
    alerts.yaml
  /schemas/
    session_envelope.v1.json
    audio_chunk.v1.json
    asr_event.v1.json
    semantic_units.v1.json
    error_model.v1.json
  /tests/
    unit/
    integration/
    golden/
  Dockerfile
  docker-compose.yaml
  README.md
```

**Giải thích file nổi bật**
- `services/asr/model_pack.json`: mô tả các tầng model, latency profile và chiến lược triển khai.
- `services/asr/verify_model_lock.py`: script kiểm tra chữ ký / integrity của model artifacts trước khi nạp.
- `schemas/*.json`: định nghĩa canonical data contracts để mọi service tuân theo cùng một schema.
- `ops/latency_profile.json`: bảng ngân sách latency cho từng giai đoạn pipeline.
- `tests/golden/`: chứa cặp audio + transcript chuẩn phục vụ regression test.
- `services/gateway/transformers/*`: chuyển đổi payload schema cũ sang phiên bản mới để backwards-compatible.

## 6 — Giới thiệu các schema (dễ hiểu + ví dụ JSON)
Tất cả schema đặt tại `/schemas`. Mỗi file gồm JSON Schema chuẩn hóa **và** ví dụ tải nhanh.

### 6.1 `session_envelope.v1.json`
Mục đích: chứa metadata chung của một session đầu vào.

Ví dụ JSON:
```json
{
  "session_id": "sess_12345",
  "device_tier": "mobile",
  "language": "vi",
  "residency": "vn",
  "llm_preset": "default",
  "tts_capability": {"device_tts_ok": true},
  "auth_token": "eyJ..",
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
}
```

### 6.2 `audio_chunk.v1.json`
```json
{
  "seq": 124,
  "timestamp_ms": 1699999999999,
  "codec": "opus",
  "duration_ms": 20,
  "base64": "...."
}
```

### 6.3 `asr_event.v1.json`
```json
{
  "type": "partial",
  "text": "xin chào",
  "confidence": 0.88,
  "segment_id": "seg_1",
  "start_ts": 1699999999000,
  "end_ts": 1699999999020
}
```

### 6.4 `semantic_units.v1.json`
```json
{
  "intent": "book_flight",
  "slots": {"destination": "Hanoi", "date": "2025-12-24"},
  "entities": [{"type": "location", "text": "Hanoi", "start": 10, "end": 15}],
  "confidence": 0.93
}
```

### 6.5 `error_model.v1.json`
```json
{
  "code": "SCHEMA_MAJORMISMATCH",
  "message": "Client schema version 0.9 not supported.",
  "retryable": false
}
```

> Tip: Sử dụng các ví dụ trên để viết integration test nhanh cho từng hop của pipeline.
