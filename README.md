# PlanT
CS361 Project

# Microservice
## Requesting Data
To request data, send a POST request to the following URL: *https://kimryan707.pythonanywhere.com/get_exercises* (URL bound to change). 

Along with the POST request, include a JSON object in the following format: *{ 'muscle category' : 'category' }*, where *category* is the muscle category for exercises that are to be returned.\
**The key for the category must be 'muscle category'**, as the microservice will search for this key.

As an example in Python:
```
import requests
import json

url = "https://kimryan707.pythonanywhere.com/get_exercises"
data = {
    'muscle category' : 'chest'
}

response = requests.get(url, params=data)
```

## Receiving Data
The microservices will return data in the form of a JSON object.

In Python:
```
if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

## UML Sequence Diagram
![Blank diagram](https://github.com/ryjn/PlanT/assets/46828676/5d94fdf7-b4f3-4105-9df7-e6ecbf72c3d9)

