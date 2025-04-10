import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import tables, reservations
from app.db import init_db

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Создание таблиц при запуске
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при старте
    init_db()
    logger.info("Database tables created.")

    yield  # Приложение работает

    # Действия при завершении
    logger.info("Shutting down the application.")


# Инициализация приложения с lifespan
app = FastAPI(lifespan=lifespan)

# Роутеры
app.include_router(tables.router, prefix="/tables", tags=["tables"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
