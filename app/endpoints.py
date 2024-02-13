from fastapi import APIRouter, HTTPException, Query

from app.wiki.frequent_words import WikiWordFrequencyAnalyser
from app.wiki.search_history import (
    check_search_history,
    get_search_history,
    save_search_history,
)

wiki_analyser = WikiWordFrequencyAnalyser()

router = APIRouter(prefix="/wiki")


@router.get("/word_analysis")
def get_wiki_frequent_words(topic: str, n: int = Query(10, gt=0, lt=100)):
    """Get the top n frequent words from the Wikipedia article."""
    
    # check if topic was searched before with name same no of frequent words
    # if so, return the record from the search history
    existing_record = check_search_history(topic, n)
    if existing_record:
        return existing_record

    # this unreliable sanity check to see if the article exists
    # this does not work well with all topics
    if not wiki_analyser.article_exists(topic):
        result = wiki_analyser.no_articles_found(topic)
        raise HTTPException(status_code=404, detail=result)

    # fetch content from the wikimedia api this is a fast process 
    # than using beautiful soup to scrape the content
    content = wiki_analyser.fetch_article_content(topic)
    
    # get the top n frequent words from the content
    # and use nltk to remove stop words
    frequent_words = wiki_analyser.get_frequent_words(content, n)
    
    # dump the to json file for future use
    record = save_search_history(topic, frequent_words)
    return record


@router.get("/search_history")
def search_history():
    """Get the search history."""
    # fetch all the search history from the json file
    # we have set a limit to the number of records to be stored 
    # in settings file.
    history = get_search_history()
    return history
