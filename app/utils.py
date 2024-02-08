import json
import os

from app.settings import settings


def check_json_file_exists():
    """Check if the json file exists."""
    # file_path = os.path.join(settings.BASE_DIR, settings.SEARCH_HISTORY_FILE)
    if os.path.isfile(settings.SEARCH_HISTORY_FILE):
        return True

    with open(settings.SEARCH_HISTORY_FILE, "w") as file:
        json.dump([], file)


def write_record_to_json_file(record):
    """Write the search history to a json file."""
    # We will use the json file to store the search history
    # this will help us to track all the queries that was made.
    try:
        # check if the file exists
        with open(settings.SEARCH_HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(record)
    with open(settings.SEARCH_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
