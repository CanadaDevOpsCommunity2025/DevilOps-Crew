import requests
import time

# Start a research task
print("Starting research task...")
r = requests.post('http://localhost:8000/research', json={'topic': 'test execution time'})
if r.status_code == 200:
    result = r.json()
    research_id = result['id']
    print(f"Research started with ID: {research_id}")

    # Wait for completion
    print("Waiting for completion...")
    while True:
        status_r = requests.get(f'http://localhost:8000/research/{research_id}')
        if status_r.status_code == 200:
            status_data = status_r.json()
            if status_data['status'] == 'completed':
                print(f"✅ Research completed! Execution time: {status_data.get('execution_time', 'N/A')} seconds")
                break
            elif status_data['status'] == 'failed':
                print("❌ Research failed")
                break
            else:
                print(f"Status: {status_data['status']}")
                time.sleep(5)
        else:
            print("Error checking status")
            break
else:
    print("Failed to start research:", r.text)
