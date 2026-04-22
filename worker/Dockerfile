# ---------- BUILD STAGE ----------
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------- PRODUCTION STAGE ----------
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime dependencies
RUN apt-get update && apt-get install -y curl procps \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY --from=builder /install /usr/local
COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

# Healthcheck needs procps (for pgrep)
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pgrep -f worker.py > /dev/null || exit 1

CMD ["python", "worker.py"]
