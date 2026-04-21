# FIXES DOCUMENTATION – Stage 2 DevOps Project

This document contains all issues discovered during development, testing, and containerization of the microservices system, along with the fixes applied.

---

## 1. Missing Health Endpoint in API

**File:** api/main.py  
**Issue:** The API did not have a `/health` endpoint, causing Docker health checks to fail.  

**Fix:** Added a simple health route.

```python
@app.get("/health")
def health():
    return {"status": "ok"}

2. Hardcoded Redis Connection in API

File: api/main.py
Issue: Redis was hardcoded to localhost, which breaks inside Docker containers.

Fix: Replaced with environment variable to allow Docker networking.
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379)

3. Worker Cannot Connect to Redis

File: worker/worker.py
Issue: Worker was also using localhost, causing connection refused errors inside Docker.

Fix: Updated worker to use environment variable.
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379)

4. Missing Redis Healthcheck

File: docker-compose.yml
Issue: Redis had no healthcheck, causing dependent services to fail startup.

Fix: Added Redis healthcheck.

healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 5s
  timeout: 3s
  retries: 5

5. API Healthcheck Failure in Docker

File: docker-compose.yml
Issue: API service lacked proper healthcheck for dependency validation.

Fix: Added Python-based healthcheck.

healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
  interval: 5s
  timeout: 3s
  retries: 5


6. Service Startup Dependency Issues

File: docker-compose.yml
Issue: Services were starting before dependencies were fully ready.

Fix: Used depends_on with service_healthy to enforce proper startup order.

7. Worker Not Processing Jobs Initially

Issue: Worker was running but not consuming jobs due to Redis misconfiguration.

Fix: Resolved after fixing Redis environment variable and ensuring correct queue usage.

8. System Architecture Validation

After fixes, the system works correctly:

API creates jobs and pushes to Redis queue
Worker consumes jobs and processes them
Redis stores job state correctly
Docker Compose manages full orchestration
All services pass health checks

Summary

The system is now fully containerized and production-ready with:

Proper service health checks
Environment-based configuration
Working Redis queue system
Worker processing system
Docker Compose orchestration with dependency management
