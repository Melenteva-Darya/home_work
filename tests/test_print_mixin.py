from src.product_classes import Product
from src.smartphone import Smartphone


def test_product_print_mixin(capsys):
    """Проверяем, что миксин логирует создание базового продукта Product."""
    Product("Тестовый товар", "Описание", 500.0, 3)

    # Перехватываем вывод print() из консоли
    captured = capsys.readouterr()

    # Проверяем наличие отладочной информации миксина
    assert "Product" in captured.out
    assert "Тестовый товар" in captured.out
    assert "500.0" in captured.out

def test_lawn_grass_mixin_log(capsys):
    """Проверяем, что миксин автоматически определяет имя класса-наследника LawnGrass."""
    Smartphone(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
        90.3,
        "Note 11",
        1024,
        "Синий",
    )

    captured = capsys.readouterr()
    assert captured.out.strip() == 'Smartphone(Xiaomi Redmi Note 11, 1024GB, Синий, 31000.0, 14)'
