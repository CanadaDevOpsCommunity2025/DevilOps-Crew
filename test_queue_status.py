from src.tv_research.worker import trend_queue, news_queue, content_queue, reporting_queue

print('trend_research:', trend_queue.count)
print('news_aggregation:', news_queue.count)
print('content_strategy:', content_queue.count)
print('final_reporting:', reporting_queue.count)

# Test Redis connection
try:
    print('Redis ping:', trend_queue.connection.ping())
except Exception as e:
    print('Redis error:', e)
