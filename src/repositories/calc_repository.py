from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DatabaseError
from src.db.models import CalcResult


class CalcRepository:
    """Репозиторий для работы с расчётами стоимости"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, total_cost_rub: float) -> CalcResult:
        """
        Сохраняет результат расчёта в базу данных
        """
        try:
            calc_result = CalcResult(total_cost_rub=Decimal(str(total_cost_rub)))
            self.session.add(calc_result)
            await self.session.commit()
            await self.session.refresh(calc_result)
            return calc_result
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseError(f"Ошибка при сохранении расчёта: {str(e)}") from e
    
    async def get_latest(self, limit: int = 10) -> list[CalcResult]:
        """
        Получает последние N расчётов, отсортированных по дате
        """
        try:
            query = select(CalcResult).order_by(CalcResult.created_at.desc()).limit(limit)
            result = await self.session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении расчётов: {str(e)}") from e

