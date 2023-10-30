import json


def load_json_file(path):
    """Retrieve data from specified path to be loaded in JSON format."""
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def write_json_file(data, path):
    """Replace data at specified path with new JSON data."""
    with open(path, 'w') as file:
        json.dump(data, file,indent=4)
    return data
