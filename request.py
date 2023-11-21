import requests
import json

url = 'http://127.0.0.1:9123/get_exercises'
data = {
    'muscle category' : 'chest'
}

response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
