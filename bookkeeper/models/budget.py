"""
Описан класс, представляющий бюджет.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
    Бюджет за определенный промежуток времени
    amount - сумма
    time - промежуток времени в днях
    budget - бюджет
    pk - id записи в базе данных
    """
    time: str
    amount: int
    budget: int = 0
    pk: int = 0