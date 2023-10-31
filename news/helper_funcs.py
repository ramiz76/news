"""Helper functions for universal use."""

import json


def load_json_file(path):
    """Retrieve data from specified path to be loaded in JSON format."""
    with open(path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data


def write_json_file(data, path):
    """Replace data at specified path with new JSON data."""
    with open(path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    return data
