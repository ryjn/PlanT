from bs4 import BeautifulSoup as bs
import re
import requests
import json
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/get_exercises', methods=['POST'])
def get_exercises():
    
    # Get JSON data from request
    req_json = request.get_json()

    # Identify muscle category
    filter = req_json["muscle category"]

    # Print receive message
    print(f"Request recieved for {filter}.")

    # Create muscle category URL
    url = "https://www.bodybuilding.com/exercises/finder/?muscle=" + filter

    # Return results of html for muscle category
    result = requests.get(url)
    site = bs(result.text, "html.parser")
    exercises = site.find_all("a", href=re.compile(r"^/exercises/"), itemprop="name")

    # Create dictionary for export JSON file
    exercise_dict = {}
    for i in range(5):
        exercise = exercises[i].string.strip()
        url = exercises[i]['href']
        exercise_dict[exercise] = {
            #exercise: {
                #"name": exercise,
                "category": filter,
                "url": "https://www.bodybuilding.com" + url
            #}
        }

    # Write results to JSON
    time.sleep(5)
    print(f"Sending exercises for {filter}.")
    return jsonify(exercise_dict)

if __name__ == '__main__':
    app.run(port=9123, debug=True)
