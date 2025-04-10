import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import tables, reservations
from app.db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("Database tables created.")

    yield

    logger.info("Shutting down the application.")


app = FastAPI(lifespan=lifespan)

# Роутеры
app.include_router(tables.router, prefix="/tables", tags=["tables"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
