import redis
import os

try:
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    r = redis.from_url(redis_url)
    print('Redis connected:', r.ping())

    # Check queues
    from rq import Queue
    queues = ['trend_research', 'news_aggregation', 'content_strategy', 'final_reporting']
    for queue_name in queues:
        queue = Queue(queue_name, connection=r)
        print(f"{queue_name}: {queue.count} jobs")

        # Check for failed jobs
        failed_queue = Queue('failed', connection=r)
        print(f"Failed jobs: {failed_queue.count}")

except Exception as e:
    print(f"Error: {e}")
