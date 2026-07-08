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
        self.__price = price
        self.quantity = quantity

        Product.number_of_product += 1

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:
            user_answer = input("Вы уверены, что хотите понизить цену? (y/n): ")
            if user_answer.lower() == 'y':
                self.__price = new_price
            else:
                print("Действие отменено")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data, current_products=None):
        if current_products:
            for existing_product in current_products:
                if product_data['name'] == existing_product.name:
                    existing_product.quantity += product_data['quantity']
                    existing_product.price = max(existing_product.price, product_data['price'])
                    return existing_product
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )


class Category:
    """Класс для категорий товаров."""

    # Аннотации типов в вашем стиле
    name: str
    description: str
    __products: list

    # Переменные на уровне класса для подсчета категорий и уникальных товаров
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.name = name
        self.description = description
        self.__products = products  # Сюда передаем список объектов класса Product

        # Автоматически увеличиваем количество категорий на 1
        Category.category_count += 1

        # Автоматически прибавляем количество переданных товаров к общему счетчику
        Category.product_count += len(products)

    def add_product(self, product):
        """Метод принимает объект класса Product и записывает его в приватный список товаров."""

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер возвращает информацию о товарах в виде строк заданного формата."""
        result = ""
        for prod in self.__products:
            # Форматируем строку строго по вашему ТЗ
            result += f"{prod.name}, {prod.price} руб. Остаток: {prod.quantity} шт.\n"
        return result
