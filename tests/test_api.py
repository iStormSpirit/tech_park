from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes import router
from src.db.database import get_db


@pytest.fixture
async def app(test_db: AsyncSession):
    """Создаём тестовое приложение с переопределёнными зависимостями"""
    app = FastAPI()
    app.include_router(router)
    
    # Переопределяем зависимость get_db для использования тестовой БД
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield app
    
    # Очищаем переопределения после теста
    app.dependency_overrides.clear()


@pytest.fixture
async def client(app: FastAPI):
    """Создаём тестового клиента"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Тест корневого эндпоинта"""
    response = await client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_calc_endpoint_success(client: AsyncClient):
    """Тест успешного расчёта стоимости"""
    payload = {
        "materials": [
            {"name": "steel", "qty": 120.0, "price_rub": 54.5},
            {"name": "copper", "qty": 12.3, "price_rub": 640.0}
        ]
    }
    
    response = await client.post("/calc", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "total_cost_rub" in data
    # Проверяем расчёт: 120 * 54.5 + 12.3 * 640 = 6540 + 7872 = 14412
    assert data["total_cost_rub"] == 14412.0


@pytest.mark.asyncio
async def test_calc_endpoint_validation_error(client: AsyncClient):
    """Тест валидации входных данных"""
    # Невалидный запрос - отрицательное количество
    payload = {
        "materials": [
            {"name": "steel", "qty": -10.0, "price_rub": 54.5}
        ]
    }
    
    response = await client.post("/calc", json=payload)
    
    assert response.status_code == 422  # Unprocessable Entity

