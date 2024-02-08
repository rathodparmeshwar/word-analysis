import re
from collections import Counter
from datetime import datetime

import nltk
import requests

from app.settings import settings
from app.utils import write_record_to_json_file


class NltkBasedStopWords:
    def __init__(
        self,
    ) -> None:
        self.stop_words = set()
        self.download_stop_words()
        self.initialize_stop_words()

    def download_stop_words(self):
        nltk.download("stopwords", download_dir=settings.NLTK_DATA_DIR)
        nltk.download("punkt", download_dir=settings.NLTK_DATA_DIR)

    def initialize_stop_words(self):
        self.stop_words = set(nltk.corpus.stopwords.words("english"))

    def filter_out_stop_words(self, words):
        filtered_stop_words = [
            word for word in words if word.lower() not in self.stop_words
        ]

        return filtered_stop_words


class WikipediaWordAnalyser(NltkBasedStopWords):
    def __init__(
        self,
    ) -> None:
        super().__init__()

    def article_exists(self, topic):
        params = {
            "action": "query",
            "titles": topic,
            "format": "json",
        }
        response = requests.get(settings.WIKIPEDIA_API_URL, params=params)
        data = response.json()
        pages = data["query"]["pages"]
        for page_id in pages.keys():
            if page_id == "-1":  # Wikipedia page doesn't exist
                return False
        return True

    def fetch_article_content(self, title: str):
        """Fetch the Wikipedia article content for the given title."""
        # reason to use media wiki api is for its fast response time,
        # we can use the wikipedia package, but it is slow
        # but its contents are more cleaner with no references etc
        params = {
            "action": "query",
            "prop": "extracts",
            "titles": title,
            "format": "json",
            "exlimit": 1,
            "explaintext": 1,
            "exsectionformat": "plain",
        }
        response = requests.get(settings.WIKIPEDIA_API_URL, params=params)
        data = response.json()
        pages = data["query"]["pages"]
        for page_id in pages.keys():
            return pages[page_id]["extract"]

        raise Exception(f"No Wikipedia article found for '{title}'")

    def get_frequent_words(self, content, n):
        """
        Get the top n frequent words.
        """
        # Using the nltk stopwords,
        # to filter out any common words that are not useful for analysis
        # Remove special characters, digits, and split into words

        text = re.sub(r"[^a-zA-Z\s]", "", content)
        words = text.split()

        # filter out the stop words
        words = self.filter_out_stop_words(words)

        word_counts = Counter(words)

        # check if we can find n number of most common words,
        # else return highest number of words found
        if len(word_counts) > n:
            top_words = word_counts.most_common(n)
        else:
            top_words = word_counts.most_common(len(word_counts))
        return dict(top_words)

    def no_articles_found(self, topic):
        """Return a message for no articles found."""
        # saving this record for past search history
        record = {
            "data": {
                "topic": topic,
                "word_count": 0,
                "frequent_words": {},
            },
            "requested_at": str(datetime.now()),
            "status": "unsuccessful",
            "message": f"No Wikipedia article found for '{topic}'",
        }
        write_record_to_json_file(record)
        return record
