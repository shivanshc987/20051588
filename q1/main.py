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
        
# A function to merge and sort a list of lists of numbers
def merge_and_sort(numbers_list):
    merged = [] # Initialize an empty list
    for numbers in numbers_list:
        merged.extend(numbers) # Extend the merged list with each numbers list
    merged = list(set(merged)) # Remove any duplicates
    merged.sort() # Sort the merged list
    return merged