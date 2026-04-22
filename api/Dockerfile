FROM python:3.12-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ FIX: combine RUN + pin packages (hadolint clean)
RUN apk add --no-cache curl=8.10.1-r0 ca-certificates=20240226-r0

RUN update-ca-certificates && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
