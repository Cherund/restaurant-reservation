import pytest
from sqlmodel import Session
from fastapi.testclient import TestClient
from app.main import app
from app.db import engine, init_db, get_session

# Создаём сессию и откатываем изменения после каждого теста
@pytest.fixture(scope="function")
def session():
    init_db()
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# Тестовый клиент FastAPI с подменённой зависимостью get_session
@pytest.fixture(scope="function")
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()
