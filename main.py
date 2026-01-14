from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.exception_handlers import (
    calc_service_error_handler,
    calculation_error_handler,
    database_error_handler,
)
from src.api.routes import router
from src.core.config.settings import app_settings
from src.core.exceptions import CalcServiceError, CalculationError, DatabaseError
from src.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=app_settings.app_name,
    description="Микросервис для расчёта стоимости изделий на основе материалов",
    lifespan=lifespan
)

# Регистрация exception handlers
app.add_exception_handler(CalculationError, calculation_error_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(CalcServiceError, calc_service_error_handler)

app.include_router(router)
