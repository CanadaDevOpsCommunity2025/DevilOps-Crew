import requests

try:
    # Test health endpoint
    r = requests.get('http://api:8000/health')
    print('Health Status:', r.status_code)
    print('Health Response:', r.text)

    # Test queue status endpoint
    r2 = requests.get('http://api:8000/queue/status')
    print('Queue Status:', r2.status_code)
    if r2.status_code == 200:
        print('Queue Response:', r2.json())
    else:
        print('Queue Response:', r2.text)

except Exception as e:
    print('Error:', e)
