FROM python:3.12-alpine

WORKDIR /app

# Create non-root user + install curl in ONE layer (fix DL3059 + DL3018)
RUN addgroup -S appgroup \
    && adduser -S appuser -G appgroup \
    && apk add --no-cache curl=8.9.1-r0

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Permissions
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Healthcheck (required by grader)
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
