from decimal import Decimal

import pytest

from src.schemas.calc import MaterialSchema
from src.services.calc_service import calculate_total_cost


def test_calculate_total_cost_success():
    """Тест успешного расчёта стоимости"""
    materials = [
        MaterialSchema(name="steel", qty=120.0, price_rub=54.5),
        MaterialSchema(name="gold", qty=12.3, price_rub=640.0)
    ]
    
    result = calculate_total_cost(materials)
    
    expected = Decimal("120.0") * Decimal("54.5") + Decimal("12.3") * Decimal("640.0")
    expected = expected.quantize(Decimal('0.01'))
    
    assert result == expected
    assert isinstance(result, Decimal)


def test_calculate_total_cost_single_material():
    """Тест расчёта для одного материала"""
    materials = [
        MaterialSchema(name="steel", qty=10.0, price_rub=100.0)
    ]
    
    result = calculate_total_cost(materials)
    
    assert result == Decimal("1000.00")


def test_calculate_total_cost_zero_quantity():
    """Тест с нулевым количеством"""
    with pytest.raises(Exception):
        MaterialSchema(name="steel", qty=0, price_rub=100.0)
