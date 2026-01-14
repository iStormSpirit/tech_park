from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.core.config import logger
from src.core.exceptions import (
    CalcServiceError,
    CalculationError,
    DatabaseError,
)


async def calculation_error_handler(request: Request, exc: CalculationError) -> JSONResponse:
    """Обработчик ошибок расчёта"""
    logger.error(f"Ошибка расчёта: {exc}", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """Обработчик ошибок базы данных"""
    logger.error(f"Ошибка БД: {exc}", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ошибка при работе с базой данных"}
    )


async def calc_service_error_handler(request: Request, exc: CalcServiceError) -> JSONResponse:
    """Обработчик общих ошибок сервиса"""
    logger.error(f"Ошибка сервиса: {exc}", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка сервиса"}
    )

