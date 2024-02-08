import json
from datetime import datetime

from app.settings import settings
from app.utils import write_record_to_json_file


def check_search_history(topic, n):
    """Check the search history."""
    with open(settings.SEARCH_HISTORY_FILE, "r") as file:
        search_history = json.load(file)
        for record in search_history:
            # check if we alreadry analyzed the topic and the analysis was successful
            if (
                record["data"]["topic"] == topic
                and record["status"] == "successful"
                and record["data"]["word_count"] == n
            ):
                return record
    return None


def get_search_history():
    """Get the search history."""
    with open(settings.SEARCH_HISTORY_FILE, "r") as file:
        search_history = json.load(file)
        if len(search_history) > settings.SEARCH_HISTORY_LIMIT:
            search_history = search_history[-settings.SEARCH_HISTORY_LIMIT :]
        return search_history


def save_search_history(topic: str, frequent_words: dict):
    """Save the search history to a file."""

    record = {
        "data": {
            "topic": topic,
            "word_count": len(frequent_words),
            "frequent_words": frequent_words,
        },
        "requested_at": str(datetime.now()),
        "status": "successful",
    }
    # Save the search history to a file
    write_record_to_json_file(record)
    return record
