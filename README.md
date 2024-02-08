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

Install test dependencies
```bash
poetry install --with test 
```

lock poetry file(development only)
```bash
poetry lock --no-update
```


#### OR - you can use pip package manager
```bash
pip install -r requirements.txt
```

#### initialize pre-commit hooks(development only)
```bash
pre-commit run --all-files
```

To start the api using the below command from root dir
```bash
uvicorn app.main:app --reload
```

## API Endpoints
#### word analysis request example
```url
http://127.0.0.1:8000/wiki/word_analysis?topic=Artificial intelligence&n=10
```
#### response example
```json
{
    "data": {
        "topic": "Artificial intelligence",
        "word_count": 10,
        "frequent_words": {
            "AI": 161,
            "intelligence": 59,
            "learning": 52,
            "used": 44,
            "artificial": 35,
            "machine": 35,
            "human": 33,
            "use": 30,
            "problems": 29,
            "research": 28
        }
    },
    "request_at": "2024-02-08 13:19:03.749992",
    "status": "successful"
}
```
#### search history request example
```url
http://127.0.0.1:8000/wiki/search_history
```
```json
[
    {
        "data" : {
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
            }
        },
        "requested_at": "2024-02-08 01:45:28.073141",
        "status": "successful"
    },
    {
        "topic": "123123",
        "requested_at": "2024-02-08 02:02:04.407498",
        "status": "unsuccessful",
        "message": "No Wikipedia article found for '123123'"
    }
]
```
#### fast api docs link - to test out the endpoints
```bash
http://127.0.0.1:8000/docs
```

#### to run tests 
```bash
pytest .
```