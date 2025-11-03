import redis
import os
from rq import Queue, FailedJobRegistry

try:
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    r = redis.from_url(redis_url)
    print('Redis connected:', r.ping())

    # Check all queues
    queues = ['trend_research', 'news_aggregation', 'content_strategy', 'final_reporting']
    for queue_name in queues:
        queue = Queue(queue_name, connection=r)
        print(f"{queue_name}: {queue.count} jobs")

        # Check failed jobs for this queue
        failed_registry = FailedJobRegistry(queue=queue)
        failed_jobs = failed_registry.get_job_ids()
        print(f"  Failed jobs: {len(failed_jobs)}")
        if failed_jobs:
            for job_id in failed_jobs:
                job = queue.fetch_job(job_id)
                if job:
                    print(f"    Failed job {job_id}: {job.exc_info}")

except Exception as e:
    print(f"Error: {e}")
