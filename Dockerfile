# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base
WORKDIR /workspace
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install shared dependencies here (left minimal for the skeleton project)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY services ./services
COPY schemas ./schemas
COPY ops ./ops
COPY requirements.txt ./requirements.txt

RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

FROM base AS runtime
CMD ["python", "services/gateway/main.py"]
