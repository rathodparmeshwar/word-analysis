# Wikipedia Word Analysis API

## Setup
#### Poetry Setup
Poetry Installation [poetry-installation](https://python-poetry.org/docs/#installation)

Creates a new virtual env for the repo
```bash
poetry shell
```
Install Dependencies

```bash
poetry install --no-root
```
#### OR - you can use pip package manager
```bash
pip install -r requirements.txt
```

To start the api using the below command from root dir
```bash
uvicorn app.main:app --reload
```

## API Endpoints
#### word analysis request example 
```url
http://127.0.0.1:8000/word_analysis?Artificial intelligence=2022&n=10
```
#### response example 
```json
{
    "topic": "2022",
    "word_count": 10,
    "frequent_words": {
        "Russian": 47,
        "Ukraine": 41,
        "invasion": 29,
        "election": 27,
        "September": 25,
        "held": 24,
        "Russia": 23,
        "Prime": 22,
        "Minister": 22,
        "United": 22
    },
    "request_at": "2024-02-08 01:45:28.073141",
    "status": "successful"
}
```
#### search history request example 
```url
http://127.0.0.1:8000/search_history
```
```json
[
    {
        "topic": "2022",
        "word_count": 10,
        "frequent_words": {
            "Russian": 47,
            "Ukraine": 41,
            "invasion": 29,
            "election": 27,
            "September": 25,
            "held": 24,
            "Russia": 23,
            "Prime": 22,
            "Minister": 22,
            "United": 22
        },
        "request_at": "2024-02-08 01:45:28.073141",
        "status": "successful"
    },
    {
        "topic": "123123",
        "request_at": "2024-02-08 02:02:04.407498",
        "status": "unsuccessful",
        "message": "No Wikipedia article found for '123123'"
    },
]
```