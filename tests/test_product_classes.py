from typing import cast

import pytest

from src.product_classes import BaseProduct, Category, Order, Product


def test_init(product_samsung):
    """Ваш тест для проверки инициализации основных атрибутов Product."""
    assert product_samsung.name == "Samsung Galaxy S23 Ultra"
    assert product_samsung.description == "256GB, Серый цвет, 200MP камера"


def test_product_price_and_quantity(product_samsung):
    """Тест для проверки цены и количества продукта."""
    assert product_samsung.price == 180000.0
    assert product_samsung.quantity == 5


def test_product_count(product_samsung, product_iphone):
    """Тест подсчета количества созданных видов продуктов."""
    # Запрошено 2 фикстуры -> создано 2 объекта Product
    assert Product.number_of_product == 2


# --- ТЕСТЫ ДЛЯ КЛАССА CATEGORY ---


def test_category_init(product_samsung, product_iphone):
    """Тест для проверки инициализации атрибутов Category."""
    products_list = [product_samsung, product_iphone]
    category = Category("Смартфоны", "Мобильные телефоны", products_list)

    assert category.name == "Смартфоны"
    assert category.description == "Мобильные телефоны"
    assert category._Category__products == products_list


def test_category_and_product_counters(product_samsung, product_iphone, product_xiaomi):
    """Тест правильности подсчета количества категорий и товаров в них."""
    # Создаем две разные категории с товарами
    Category("Флагманы", "Дорогие телефоны", [product_samsung, product_iphone])
    Category("Бюджетники", "Дешевые телефоны", [product_xiaomi])

    # Проверяем сквозные счетчики классов
    assert Category.category_count == 2  # Всего создано 2 категории
    assert Category.product_count == 3  # Внутри категорий суммарно 3 товара


def test_product_price_setter(capsys):
    prod = Product("Тест", "Описание", 100.0, 10)

    # Проверяем запрет отрицательной цены
    prod.price = -10
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_new_product_duplicate():
    p1 = Product("Нокиа", "Старый", 1000.0, 2)
    data = {"name": "Нокиа", "description": "Новый", "price": 1500.0, "quantity": 3}

    # Вызываем слияние
    updated = Product.new_product(data, [p1])

    assert updated.quantity == 5  # 2 + 3
    assert updated.price == 1500.0  # max(1000, 1500)


def test_product_price_decrease(monkeypatch, capsys):
    prod = Product("Тест", "Описание", 100.0, 10)

    # Имитируем, что пользователь ввел 'y' (согласие на понижение)
    monkeypatch.setattr("builtins.input", lambda _: "y")

    prod.price = 80.0  # Понижаем цену
    assert prod.price == 80.0


def test_product_price_decrease_canceled(monkeypatch, capsys):
    """Тест отмены понижения цены (пользователь вводит 'n')."""
    prod = Product("Тест", "Описание", 100.0, 10)

    # Имитируем, что пользователь отказался (ввел 'n')
    monkeypatch.setattr("builtins.input", lambda _: "n")

    prod.price = 80.0  # Пытаемся понизить цену
    captured = capsys.readouterr()

    assert "Действие отменено" in captured.out
    assert prod.price == 100.0  # Цена ДОЛЖНА остаться старой


def test_category_add_product(product_samsung, product_xiaomi):
    """Тест метода add_product в классе Category."""
    category = Category("Смартфоны", "Тест", [product_samsung])

    # Изначально 1 товар в категории
    assert Category.product_count == 1

    # Добавляем второй товар через метод
    category.add_product(product_xiaomi)

    # Проверяем, что счетчик увеличился, а товар внутри приватного списка
    assert Category.product_count == 2
    assert product_xiaomi in category._Category__products


def test_product_str(product_samsung):
    """Тест магического метода __str__ класса Product."""
    # Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.
    expected_str = "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
    assert str(product_samsung) == expected_str


def test_category_str_and_products_getter(product_samsung, product_iphone):
    """Тест метода __str__ и геттера products класса Category."""
    category = Category("Смартфоны", "Тест", [product_samsung, product_iphone])

    # 1. Проверяем __str__ категории (суммарное количество штук: 5 + 8 = 13)
    assert str(category) == "Смартфоны, количество продуктов: 13 шт."

    # 2. Проверяем геттер строк продуктов
    products_output = category.products
    assert "Samsung Galaxy S23 Ultra" in products_output
    assert "Iphone 15" in products_output


def test_add_product_wrong_type() -> None:
    """Тест проверяет, что при передаче строки вместо продукта вызывается TypeError."""
    category = Category("Смартфоны", "Категория смартфонов", [])

    # Оборачиваем вызов метода, чтобы pytest знал, что мы ждем ошибку TypeError
    with pytest.raises(TypeError):
        # cast обманывает mypy/PyCharm, чтобы они не ругались на тип аргумента
        fake_product = cast(Product, "Просто строка вместо продукта")
        category.add_product(fake_product)


def test_base_product_instantiation_error():
    """Проверяем, что нельзя создать объект абстрактного класса напрямую."""
    with pytest.raises(TypeError):
        BaseProduct()  # type: ignore[abstract]


def test_empty_subclass_is_forbidden():
    """Тест проверяет, что незавершенный наследник вызовет ошибку."""

    # noinspection PyAbstractClass
    class FakeProduct(BaseProduct):  # type: ignore[abstract]
        pass

    # Пытаемся создать объект пустого класса — вот тут Python выдаст TypeError!
    with pytest.raises(TypeError):
        FakeProduct()  # type: ignore[abstract]


def test_add_product_zero_quantity(capsys):
    """Тест: Проверяет логику try-except-else-finally при добавлении некорректного товара в Категорию."""
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый", 180000.0, 5)
    category = Category("Смартфоны", "Категория смартфонов", [product1])

    # Сначала сбросим буфер вывода, чтобы убрать принты от создания миксинов
    capsys.readouterr()

    # Создаем товар с нулевым количеством
    bad_product = Product("Бракованный товар", "Неверное количество", 1000.0, 0)

    # Вызываем метод, где отрабатывает try-except-else-finally
    category.add_product(bad_product)

    # Перехватываем то, что напечатал метод add_product
    captured = capsys.readouterr()

    # Проверяем, что в консоли появились нужные строки из блоков except и finally
    assert (
        "Попытка добавить товар с нулевым или отрицательным количеством" in captured.out
    )
    assert "Обработка добавления товара завершена" in captured.out


def test_add_product_success(capsys):
    """Тест: Проверяет логику успешного добавления товара (блок else и finally)."""
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый", 180000.0, 5)
    category = Category("Смартфоны", "Категория смартфонов", [])

    capsys.readouterr()  # Очищаем старые принты
    category.add_product(product1)

    captured = capsys.readouterr()
    # Проверяем строки из блоков else и finally
    assert "Товар добавлен успешно" in captured.out
    assert "Обработка добавления товара завершена" in captured.out


def test_order_zero_quantity_exception(capsys):
    """Тест: Проверяет логику try-except-finally при создании некорректного заказа."""
    product = Product("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5)

    capsys.readouterr()  # Очищаем принты миксинов

    # Создаем заказ с количеством 0
    Order("Новый заказ", "Покупка", product, 0)

    captured = capsys.readouterr()
    # Проверяем строки из блоков except и finally в Order
    assert "Заказ не может содержать 0 или меньше единиц товара" in captured.out
    assert "Обработка добавления товара завершена" in captured.out
