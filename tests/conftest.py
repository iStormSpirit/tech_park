import pytest
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import StaticPool

from src.db.models import Base
from src.repositories.calc_repository import CalcRepository


@pytest.fixture(scope="function")
async def test_db_engine():
    """Создаёт тестовый движок БД в памяти"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_db(test_db_engine):
    """Создаёт тестовую сессию БД"""
    async_session_maker = async_sessionmaker(
        test_db_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session


@pytest.fixture
def repository(test_db: AsyncSession):
    """Фикстура для репозитория"""
    return CalcRepository(test_db)

