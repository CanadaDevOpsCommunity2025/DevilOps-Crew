import redis
import os
from rq import Queue

try:
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    r = redis.from_url(redis_url)
    print('Redis connected:', r.ping())

    # Check news aggregation queue
    news_queue = Queue('news_aggregation', connection=r)
    print(f"News aggregation queue has {news_queue.count} jobs")

    if news_queue.count > 0:
        # Get the job
        job = news_queue.jobs[0]  # Get first job
        print(f"Job ID: {job.id}")
        print(f"Job function: {job.func_name}")
        print(f"Job args: {job.args}")
        print(f"Job kwargs: {job.kwargs}")
        print(f"Job status: {job.get_status()}")

        # Try to get job data
        try:
            job.refresh()
            print(f"Job meta: {job.meta}")
        except Exception as e:
            print(f"Error getting job meta: {e}")

except Exception as e:
    print(f"Error: {e}")
