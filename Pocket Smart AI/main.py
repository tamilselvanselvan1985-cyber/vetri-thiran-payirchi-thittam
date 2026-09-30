from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from database import init_db

from config import (
    APP_NAME,
    ALLOWED_ORIGINS
)

from app.routes import (
    pages,
    auth,
    planners
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=ALLOWED_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static"
)


app.include_router(
    pages.router
)


app.include_router(
    auth.router,
    prefix="/api"
)


app.include_router(
    planners.router,
    prefix="/api"
)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": APP_NAME
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )