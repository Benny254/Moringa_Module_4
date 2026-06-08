import json
import os

DATA_DIR = "data"

def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)