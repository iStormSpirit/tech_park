import time
from decimal import Decimal

import pytest

from src.repositories.calc_repository import CalcRepository


@pytest.mark.asyncio
async def test_create_calc_result(repository: CalcRepository):
    total_cost = 1000.50
    
    result = await repository.create(total_cost)
    
    assert result.id is not None
    assert result.total_cost_rub == Decimal(str(total_cost))
    assert result.created_at is not None


@pytest.mark.asyncio
async def test_get_latest_calculations(repository: CalcRepository):
    """Тест получения последних расчётов и ограничения количества записей """
    for i in range(5):
        await repository.create(float(100 * (i + 1)))
        # Необходима задержка т.к. иначе все записи будут с одним временем.
        time.sleep(1)
    
    results = await repository.get_latest(limit=3)
    assert len(results) == 3

    assert results[0].total_cost_rub == Decimal("500.0")
    assert results[-1].total_cost_rub == Decimal("300.0")

