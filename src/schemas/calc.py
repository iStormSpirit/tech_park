from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_serializer


class MaterialSchema(BaseModel):
    name: str = Field(..., description="Название материала")
    qty: float = Field(..., gt=0, description="Количество материала")
    price_rub: float = Field(..., gt=0, description="Цена за единицу в рублях")


class CalcRequestSchema(BaseModel):
    materials: list[MaterialSchema] = Field(..., min_length=1, description="Список материалов")


class CalcResponseSchema(BaseModel):
    total_cost_rub: Decimal = Field(..., description="Общая стоимость в рублях")
    
    @field_serializer('total_cost_rub')
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)


class CalcResultItemSchema(BaseModel):
    id: int = Field(..., description="ID расчёта")
    total_cost_rub: Decimal = Field(..., description="Общая стоимость в рублях")
    created_at: datetime = Field(..., description="Дата создания")
    
    @field_serializer('total_cost_rub')
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)
    
    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        return value.isoformat()
