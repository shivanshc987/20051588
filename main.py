import requests
import json
from flask import Flask, request, jsonify
from threading import Thread
from queue import Queue

app = Flask(__name__)

# A function to fetch numbers from a given URL and put them in a queue
def fetch_numbers(url, queue):
    try:
        response = requests.get(url, timeout=1) # Set timeout to 1 seconds
        if response.status_code == 200:
            data = response.json()
            if "numbers" in data and isinstance(data["numbers"], list):
                queue.put(data["numbers"]) # Put the numbers list in the queue
    except Exception as e:
        print(e) # Handle any exceptions