import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


WORD_ANALYSER_URL = "/wiki/word_analysis"
SEARCH_HISTORY_URL = "/wiki/search_history"


def test_validation_exception_with_string_n_input(client):
    response = client.get(f"{WORD_ANALYSER_URL}?topic=123123&n=python")
    json_response = response.json()
    assert response.status_code == 422  # 422 Unprocessable Entity
    assert "field" in json_response
    assert "message" in json_response
    assert "type" in json_response
    assert json_response["field"] == "n"
    assert (
        json_response["message"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )


def test_validation_exception_with_negative_n_input(client):
    response = client.get(f"{WORD_ANALYSER_URL}?topic=Artificial intelligence&n=-1")
    json_response = response.json()

    assert response.status_code == 422
    assert "field" in json_response
    assert "message" in json_response
    assert "type" in json_response

    assert json_response["field"] == "n"
    assert json_response["message"] == "Input should be greater than 0"
    assert json_response["type"] == "greater_than"


def test_validation_exception_with_large_n_input(client):
    response = client.get(f"{WORD_ANALYSER_URL}?topic=Artificial intelligence&n=101")
    json_response = response.json()

    assert response.status_code == 422  # 422 Unprocessable Entity
    assert "field" in json_response
    assert "message" in json_response
    assert "type" in json_response

    assert json_response["field"] == "n"
    assert json_response["message"] == "Input should be less than 100"
    assert json_response["type"] == "less_than"


def test_validation_exc_with_float_n_input(client):
    response = client.get(f"{WORD_ANALYSER_URL}?topic=Artificial intelligence&n=10.5")
    json_response = response.json()

    assert response.status_code == 422  # 422 Unprocessable Entity
    assert "field" in json_response
    assert "message" in json_response
    assert "type" in json_response

    assert json_response["field"] == "n"
    assert (
        json_response["message"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )
    assert json_response["type"] == "int_parsing"


def test_no_article_found(client):
    response = client.get(f"{WORD_ANALYSER_URL}?topic=123123&n=10")
    json_response = response.json()
    assert response.status_code == 404
    assert "detail" in json_response
    assert json_response["detail"]["status"] == "unsuccessful"


def test_article_with_integers(client):
    response = client.get(f"{WORD_ANALYSER_URL}?topic=2022&n=10")
    json_response = response.json()
    # print(json_response)
    assert response.status_code == 200
    assert "frequent_words" in json_response["data"]
    assert "status" in json_response
    assert json_response["status"] == "successful"


def test_article_with_special_characters(client):
    response = client.get(f"{WORD_ANALYSER_URL}?topic=@%$$$&n=10")
    json_response = response.json()
    assert response.status_code == 404
    assert "detail" in json_response
    assert "status" in json_response["detail"]
    assert json_response["detail"]["status"] == "unsuccessful"


def test_article_with_valid_special_characters(client):
    response = client.get(f"{WORD_ANALYSER_URL}?topic=Artificial_intelligence&n=10")
    json_response = response.json()
    assert response.status_code == 200
    assert "frequent_words" in json_response["data"]
    assert "status" in json_response
    assert json_response["status"] == "successful"


def test_article_with_alpha_numeric(client):
    response = client.get(f"{WORD_ANALYSER_URL}?topic=World War 2&n=10")
    json_response = response.json()
    assert response.status_code == 200
    assert "frequent_words" in json_response["data"]
    assert "status" in json_response
    assert json_response["status"] == "successful"


def test_search_history(client):
    response = client.get(f"{SEARCH_HISTORY_URL}")
    json_response = response.json()
    assert isinstance(json_response, list)
