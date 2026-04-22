import redis
import os
import time


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)


def process_job(job_id):
    print(f"Processing job {job_id}")

    time.sleep(2)

    r.hset(f"job:{job_id}", "status", "completed")

    print(f"Done: {job_id}")


print("Worker started...")


while True:
    try:
        job = r.brpop("job", timeout=5)

        if job:
            _, job_id = job
            job_id = job_id.decode() if isinstance(job_id, bytes) else job_id
            process_job(job_id)
        else:
            print("No job, retrying...")

    except Exception as e:
        print("Worker error:", e)
        time.sleep(2)
