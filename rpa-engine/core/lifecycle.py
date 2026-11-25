from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def rpa_lifespan(app: FastAPI):
    app.state.rpa_engine_ready = True
    yield
    app.state.rpa_engine_ready = False
