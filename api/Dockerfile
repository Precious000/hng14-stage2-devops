# ---------- Stage 1: Builder ----------
FROM python:3.12-alpine AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# build dependencies (version-pinned to satisfy hadolint)
RUN apk add --no-cache \
    build-base=0.5-r3

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# runtime deps only (version-pinned to satisfy hadolint)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup \
    && apk add --no-cache \
    curl=8.10.1-r0 \
    ca-certificates=20241010-r0 \
    wget=1.24.5-r0 \
    && update-ca-certificates

# copy installed python packages
COPY --from=builder /install /usr/local

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
