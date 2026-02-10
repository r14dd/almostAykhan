from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backer.db import initialize
from backer.routes.ask import router as ask_router
from backer.routes.health import router as health_router
from backer.routes.ingest_route import router as ingest_router
from backer.routes.stats import router as stats_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    initialize()
    yield


app = FastAPI(lifespan=lifespan)

# Serve frontend files at /ui
app.mount("/ui", StaticFiles(directory="fronter", html=True), name="ui")

app.include_router(health_router)
app.include_router(ask_router)
app.include_router(stats_router)
app.include_router(ingest_router)
