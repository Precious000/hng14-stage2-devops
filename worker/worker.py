import redis
import os
import time
import uuid


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379
)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "done")
    print(f"Done: {job_id}")


print("Worker started...")


while True:
    job = r.brpop("job", timeout=5)
    if job:
        _, job_id = job
        job_id = job_id.decode()
        process_job(job_id)
