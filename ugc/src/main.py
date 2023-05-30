import logging

import uvicorn
from api.v1 import films_reviews
from core.config import project_settings
from db import mongo
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=project_settings.UGC_PROJECT_NAME,
    description="API для работы с пользовательским контентом",
    version=project_settings.UGC_PROJECT_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    mongo.mongo = mongo.Mongo(
        f"mongodb://{project_settings.MONGOS1_HOST}:{project_settings.MONGOS1_PORT}, \
                    {project_settings.MONGOS2_HOST}:{project_settings.MONGOS2_PORT}"
    )


@app.on_event("shutdown")
async def shutdown():
    mongo.mongo.close()


app.include_router(
    films_reviews.router,
    prefix="/api/v1/films/review",
    tags=["Рецензии фильмов"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, log_level=logging.DEBUG)
