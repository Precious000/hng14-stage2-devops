FROM python:3.12-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ CRITICAL FIX: curl + SSL certs for healthcheck
RUN apk add --no-cache curl ca-certificates

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# safer + SSL-safe healthcheck
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
