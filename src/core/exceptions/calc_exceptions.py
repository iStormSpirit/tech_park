"""Исключения для калькулятора стоимости"""


class CalcServiceError(Exception):
    """Базовое исключение для сервиса калькулятора"""
    pass


class CalculationError(CalcServiceError):
    """Ошибка при расчёте стоимости"""
    pass


class DatabaseError(CalcServiceError):
    """Ошибка работы с базой данных"""
    pass

