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

# A route to handle the GET /numbers API
@app.route("/numbers", methods=["GET"])
def numbers():
    urls = request.args.getlist("url") # Get the list of URLs from query parameters
    queue = Queue() # Initialize a queue to store the numbers from each URL
    threads = [] # Initialize a list to store the threads for each URL

    for url in urls:
        if url.startswith("http"): # Check if the URL is valid
            thread = Thread(target=fetch_numbers, args=(url, queue)) # Create a thread to fetch numbers from the URL
            thread.start() # Start the thread
            threads.append(thread) # Append the thread to the list

    for thread in threads:
        thread.join() # Wait for all threads to finish

    numbers_list = [] # Initialize an empty list to store the numbers from the queue
    while not queue.empty():
        numbers_list.append(queue.get()) # Get the numbers list from the queue and append it to the list

    result = merge_and_sort(numbers_list) # Merge and sort the numbers list

    return jsonify({"numbers": result}) # Return the JSON response with the result

if __name__ == "__main__":
    app.run(port=8008) # Run the app on port 8008
