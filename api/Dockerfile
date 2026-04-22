FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
RUN addgroup -S appgroup \
    && adduser -S appuser -G appgroup \
    && apk add --no-cache curl ca-certificates \
    && update-ca-certificates

COPY requirements.txt .

# Upgrade pip + install deps
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Healthcheck (safe + reliable)
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:8000/health || exit 1

# ✅ FIXED CMD (THIS WAS BROKEN)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
