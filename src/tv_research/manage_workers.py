#!/usr/bin/env python
"""
Worker management script for TV Research application.
This script helps manage and monitor Redis Queue workers.
"""

import os
import sys
import subprocess
import signal
import time
from typing import List, Optional
import argparse

def start_worker(queue_name: str, worker_id: Optional[str] = None) -> subprocess.Popen:
    """Start a worker process for a specific queue"""
    env = os.environ.copy()
    env['WORKER_QUEUE'] = queue_name

    if worker_id:
        env['WORKER_ID'] = worker_id

    cmd = [sys.executable, 'src/tv_research/worker.py']

    print(f"Starting worker for queue: {queue_name}")
    process = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return process

def start_all_workers():
    """Start workers for all queues"""
    workers = []

    # Start multiple trend research workers
    for i in range(2):
        worker = start_worker('trend_research', f'trend-{i+1}')
        workers.append(('trend_research', worker))

    # Start multiple news aggregation workers
    for i in range(2):
        worker = start_worker('news_aggregation', f'news-{i+1}')
        workers.append(('news_aggregation', worker))

    # Start content strategy worker
    worker = start_worker('content_strategy', 'content-1')
    workers.append(('content_strategy', worker))

    # Start final reporting worker
    worker = start_worker('final_reporting', 'reporting-1')
    workers.append(('final_reporting', worker))

    return workers

def monitor_workers(workers: List[tuple]):
    """Monitor worker processes"""
    try:
        while True:
            time.sleep(5)
            for queue_name, process in workers:
                if process.poll() is not None:
                    print(f"Worker for {queue_name} exited with code {process.returncode}")
                    # Restart worker
                    new_worker = start_worker(queue_name)
                    workers[workers.index((queue_name, process))] = (queue_name, new_worker)

    except KeyboardInterrupt:
        print("Shutting down workers...")
        for queue_name, process in workers:
            process.terminate()

        # Wait for graceful shutdown
        time.sleep(2)
        for queue_name, process in workers:
            if process.poll() is None:
                process.kill()

def main():
    parser = argparse.ArgumentParser(description='Manage TV Research workers')
    parser.add_argument('action', choices=['start', 'monitor', 'status'],
                       help='Action to perform')
    parser.add_argument('--queue', help='Specific queue to manage')
    parser.add_argument('--workers', type=int, default=1,
                       help='Number of workers to start (for start action)')

    args = parser.parse_args()

    if args.action == 'start':
        if args.queue:
            # Start workers for specific queue
            workers = []
            for i in range(args.workers):
                worker_id = f"{args.queue}-{i+1}" if args.workers > 1 else None
                worker = start_worker(args.queue, worker_id)
                workers.append((args.queue, worker))

            if args.workers == 1:
                # Just run single worker
                try:
                    worker[1].wait()
                except KeyboardInterrupt:
                    worker[1].terminate()
            else:
                # Monitor multiple workers
                monitor_workers(workers)

        else:
            # Start all workers
            workers = start_all_workers()
            monitor_workers(workers)

    elif args.action == 'monitor':
        # This would require keeping track of running workers
        print("Monitoring functionality requires workers to be started first")
        print("Use: python manage_workers.py start")

    elif args.action == 'status':
        # Check Redis queue status
        try:
            import redis
            from rq import Queue

            redis_conn = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))

            queues = ['trend_research', 'news_aggregation', 'content_strategy', 'final_reporting']
            for queue_name in queues:
                queue = Queue(queue_name, connection=redis_conn)
                print(f"{queue_name}: {queue.count} jobs")

        except ImportError:
            print("Redis/RQ not available. Make sure dependencies are installed.")
        except Exception as e:
            print(f"Error checking status: {e}")

if __name__ == '__main__':
    main()
