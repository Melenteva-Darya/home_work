class Product:
    """Класс для продуктов."""

    # Аннотации типов в вашем стиле
    name: str
    description: str
    price: float
    quantity: int

    # Переменная на уровне класса для подсчета количества видов продуктов
    number_of_product = 0

    def __init__(self, name, description, price, quantity):
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

        Product.number_of_product += 1


class Category:
    """Класс для категорий товаров."""

    # Аннотации типов в вашем стиле
    name: str
    description: str
    products: list

    # Переменные на уровне класса для подсчета категорий и уникальных товаров
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.name = name
        self.description = description
        self.products = products  # Сюда передаем список объектов класса Product

        # Автоматически увеличиваем количество категорий на 1
        Category.category_count += 1

        # Автоматически прибавляем количество переданных товаров к общему счетчику
        Category.product_count += len(products)
