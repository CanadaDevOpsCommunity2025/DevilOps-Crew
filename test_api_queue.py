import requests

try:
    r = requests.get('http://localhost:8000/queue/status')
    print('Status:', r.status_code)
    if r.status_code == 200:
        print('Response:', r.json())
    else:
        print('Response:', r.text)
except Exception as e:
    print('Error:', e)
