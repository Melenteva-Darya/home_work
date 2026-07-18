import pytest

from src.lawngrass import LawnGrass
from src.product_classes import Category
from src.product_classes import Product
from src.smartphone import Smartphone


@pytest.fixture(autouse=True)
def reset_counters():
    """Автоматически сбрасывает счетчики классов перед каждым тестом,

    чтобы тесты были изолированными и независимыми.
    """
    Product.number_of_product = 0
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product_samsung():
    """Фикстура для смартфона Samsung."""
    return Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )


@pytest.fixture
def product_iphone():
    """Фикстура для смартфона iPhone."""
    return Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
    )


@pytest.fixture
def product_xiaomi():
    """Фикстура для смартфона Xiaomi."""
    return Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
    )


@pytest.fixture
def smartphone1():
    """Фикстура для модуля "Cмартфон" Samsung Galaxy S23 Ultra."""
    return Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )


@pytest.fixture
def smartphone2():
    """Фикстура для модуля "Cмартфон" Iphone 15."""
    return Smartphone(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
        98.2,
        "15",
        512,
        "Gray space",
    )


@pytest.fixture
def smartphone3():
    """Фикстура для модуля "Cмартфон" Xiaomi Redmi Note 11."""
    return Smartphone(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
        90.3,
        "Note 11",
        1024,
        "Синий",
    )


@pytest.fixture
def lawngrass_1():
    """Фикстура для модуля "Трава газонная" Газонная трава 1."""
    return LawnGrass(
        "Газонная трава 1",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )


@pytest.fixture
def lawngrass_2():
    """Фикстура для модуля "Трава газонная" Газонная трава 2."""
    return LawnGrass(
        "Газонная трава 2",
        "Выносливая трава",
        450.0,
        15,
        "США",
        "5 дней",
        "Темно-зеленый",
    )
