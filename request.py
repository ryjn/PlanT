import requests
import json

url = "https://kimryan707.pythonanywhere.com/get_exercises"
data = {
    'muscle category' : 'chest'
}

response = requests.get(url, params=data)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
