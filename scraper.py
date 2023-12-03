from bs4 import BeautifulSoup as bs
import re
import requests
import json
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def get_exercises():
    # Identify muscle category
    exercise_cat = str(request.args.get("muscle category"))

    # Create muscle category URL
    url = "https://www.bodybuilding.com/exercises/finder/?muscle=" + exercise_cat


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
                "category": exercise_cat,
                "url": "https://www.bodybuilding.com" + url

        }

    # Write results to JSON
    json_dump = json.dumps(exercise_dict)
    return json_dump