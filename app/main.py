from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.endpoints import router as wiki_router
from app.settings import settings
from app.utils import check_json_file_exists

# check if the json file exists, else create one
check_json_file_exists()


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(wiki_router, tags=["wiki"])


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    details = {
        "field": exc.errors()[0]["loc"][1],
        "message": exc.errors()[0]["msg"],
        "type": exc.errors()[0]["type"],
    }
    return JSONResponse(content=details, status_code=422)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
