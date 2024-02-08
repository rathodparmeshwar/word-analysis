from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Words Analysis API"
    PROJECT_VERSION: str = "1.0.0"

    WIKIPEDIA_API_URL: str = "https://en.wikipedia.org/w/api.php"
    SEARCH_HISTORY_FILE: str = "data/search_history.json"
    SEARCH_HISTORY_LIMIT: int = 20

    NLTK_DATA_DIR: str = "data/nltk_data"


settings = Settings()
