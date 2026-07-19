from abc import ABC, abstractmethod


class BaseProduct(ABC):

    @classmethod
    @abstractmethod
    def new_product(cls, *args, **kwargs):
        pass


class BaseStorage(ABC):
    """Абстрактный базовый класс для хранения и учета объектов."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self) -> str:
        """Обязательный метод для строкового представления во всех подклассах."""
        pass
