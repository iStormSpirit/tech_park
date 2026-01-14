from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.repositories.calc_repository import CalcRepository


def get_repository(db: AsyncSession = Depends(get_db)) -> CalcRepository:
    """Dependency для получения репозитория"""
    return CalcRepository(db)
