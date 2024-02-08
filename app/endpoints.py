from fastapi import APIRouter, HTTPException, Query

from app.wiki.analyse_words import WikipediaWordAnalyser
from app.wiki.search_history import (
    check_search_history,
    get_search_history,
    save_search_history,
)

wiki_analyser = WikipediaWordAnalyser()

router = APIRouter(prefix="/wiki")


@router.get("/word_analysis")
def get_wiki_frequent_words(topic: str, n: int = Query(10, gt=0, lt=100)):
    """Get the top n frequent words from the Wikipedia article."""
    existing_record = check_search_history(topic, n)
    if existing_record:
        return existing_record

    if not wiki_analyser.article_exists(topic):
        result = wiki_analyser.no_articles_found(topic)
        raise HTTPException(status_code=404, detail=result)

    content = wiki_analyser.fetch_article_content(topic)
    frequent_words = wiki_analyser.get_frequent_words(content, n)
    record = save_search_history(topic, frequent_words)
    return record


@router.get("/search_history")
def search_history():
    """Get the search history."""
    search_history = get_search_history()
    return search_history
