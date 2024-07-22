import json

def read_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config