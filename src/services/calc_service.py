from decimal import Decimal

from src.core.config import logger
from src.core.exceptions import CalculationError
from src.schemas.calc import MaterialSchema


def calculate_total_cost(materials: list[MaterialSchema]) -> Decimal:
    """
    Рассчитывает общую стоимость материалов
    """
    try:
        total = sum(
            Decimal(str(material.qty)) * Decimal(str(material.price_rub))
            for material in materials
        )
        result = Decimal(str(total)).quantize(Decimal('0.01'))
        logger.info(f"Рассчитана стоимость: {result} руб. для {len(materials)} материалов")
        return result
    except (ValueError, TypeError) as e:
        logger.error(f"Ошибка при расчёте стоимости: {e}")
        raise CalculationError(f"Ошибка при расчёте стоимости: {str(e)}") from e
