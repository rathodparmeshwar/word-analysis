import pytest

from app.wiki.analyse_words import WikipediaWordAnalyser

wiki_analyser = WikipediaWordAnalyser()


@pytest.mark.parametrize(
    "article_id, status",
    [("NONEXISTENT_PAGE", False), ("Python (programming language)", True)],
)
def test_article_exits(article_id, status):
    assert wiki_analyser.article_exists(article_id) == status


@pytest.mark.parametrize("article", ["NONEXISTENT_PAGE", "Pyth", ""])
def test_no_article_found(article):
    with pytest.raises(KeyError):
        wiki_analyser.fetch_article_content(article)


@pytest.mark.parametrize(
    "article", ["Python (programming language)", "Artificial intelligence"]
)
def test_article_found(article):
    response = wiki_analyser.fetch_article_content(article)
    assert response is not None
    assert len(response) > 0


@pytest.mark.parametrize(
    "article", ["Python (programming language)", "Artificial intelligence"]
)
def test_top_frequent_words(article):
    n = 10
    response = wiki_analyser.fetch_article_content(article)
    result = wiki_analyser.get_frequent_words(response, n)
    assert len(result) == n
    assert isinstance(result, dict)
    assert all(isinstance(key, str) for key in result.keys())
    assert all(isinstance(value, int) for value in result.values())
