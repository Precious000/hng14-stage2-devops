# -------- Stage 1: Build dependencies --------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# -------- Stage 2: Runtime --------
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy app code
COPY . .

# Set permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Optional: environment variable for worker behavior
ENV PYTHONUNBUFFERED=1

# Healthcheck (VERY IMPORTANT)
# This assumes your worker stays alive and can be probed
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pgrep -f worker.py || exit 1

# Run the worker
CMD ["python", "worker.py"]
