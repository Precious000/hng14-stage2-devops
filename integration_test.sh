#!/bin/bash
set -e

BASE_URL="http://localhost:8000"
TIMEOUT=60
INTERVAL=2

echo "Waiting for API to be healthy..."
elapsed=0
until curl -sf "$BASE_URL/health" | grep -q "ok"; do
  if [ "$elapsed" -ge "$TIMEOUT" ]; then
    echo "ERROR: API did not become healthy within ${TIMEOUT}s"
    exit 1
  fi
  sleep $INTERVAL
  elapsed=$((elapsed + INTERVAL))
done
echo "API is healthy."

echo "Creating job..."
JOB_ID=$(curl -sf -X POST "$BASE_URL/jobs" | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job created: $JOB_ID"

echo "Polling for completion..."
elapsed=0
until [ "$(curl -sf "$BASE_URL/jobs/$JOB_ID" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")" = "completed" ]; do
  if [ "$elapsed" -ge "$TIMEOUT" ]; then
    echo "ERROR: Job $JOB_ID did not complete within ${TIMEOUT}s"
    exit 1
  fi
  sleep $INTERVAL
  elapsed=$((elapsed + INTERVAL))
done

echo "Job $JOB_ID completed successfully."
