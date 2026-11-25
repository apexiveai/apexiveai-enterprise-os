from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def ai_lifespan(app: FastAPI):
    app.state.ai_engine_ready = True
    yield
    app.state.ai_engine_ready = False
