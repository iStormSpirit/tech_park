from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_repository
from src.core.config import logger
from src.repositories.calc_repository import CalcRepository
from src.schemas.calc import (CalcRequestSchema, CalcResponseSchema,
                              CalcResultItemSchema)
from src.services.calc_service import calculate_total_cost

router = APIRouter()


@router.post("/calc", response_model=CalcResponseSchema, status_code=status.HTTP_201_CREATED)
async def calculate_cost(
        request: CalcRequestSchema,
        repository: CalcRepository = Depends(get_repository)
):
    """
    Рассчитывает стоимость изделия на основе материалов
    """
    logger.info(f"Получен запрос на расчёт стоимости для {len(request.materials)} материалов")
    total_cost = calculate_total_cost(request.materials)
    calc_result = await repository.create(float(total_cost))
    logger.info(f"Расчёт сохранён в БД с ID: {calc_result.id}")
    return CalcResponseSchema(total_cost_rub=total_cost)


@router.get("/last_calc", response_model=list[CalcResultItemSchema])
async def last_calc(
        repository: CalcRepository = Depends(get_repository)
):
    """
    Возвращает 10 последних расчётов отсортированных по дате
    """
    logger.info("Получен запрос на список последних расчётов")
    results = await repository.get_latest(limit=10)
    logger.info(f"Возвращено {len(results)} расчётов")
    return [
        CalcResultItemSchema(
            id=result.id,
            total_cost_rub=result.total_cost_rub,
            created_at=result.created_at
        )
        for result in results
    ]


@router.get("/")
async def root():
    return {"message": "Сервис расчёта стоимости изделия"}
