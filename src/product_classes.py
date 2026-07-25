from src.baseabstract import BaseProduct, BaseStorage
from src.exception import ZeroQuantity
from src.print_mixin import PrintMixin


class Product(BaseProduct, PrintMixin):
    """Класс для продуктов."""

    name: str
    description: str
    __price: float
    quantity: int
    number_of_product = 0

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

        Product.number_of_product += 1
        super().__init__()

    @classmethod
    def new_product(cls, product_data, current_products=None):
        """Класс-метод для создания нового товара или обновления дубликата."""
        if current_products:
            for existing_product in current_products:
                if product_data["name"] == existing_product.name:
                    existing_product.quantity += product_data["quantity"]
                    existing_product.price = max(
                        existing_product.price, product_data["price"]
                    )
                    return existing_product
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:
            user_answer = input("Вы уверены, что хотите понизить цену? (y/n): ")
            if user_answer.lower() == "y":
                self.__price = new_price
            else:
                print("Действие отменено")
        else:
            self.__price = new_price

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(other) is Product:
            result_sum = self.price * self.quantity + other.price * other.quantity
            return result_sum
        raise TypeError


class Category(BaseStorage):
    """Класс для категорий товаров."""

    name: str
    description: str
    __products: list
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        super().__init__(name, description)
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product):
        if isinstance(product, Product):
            try:
                if product.quantity <= 0:
                    raise ZeroQuantity(
                        "Попытка добавить товар с нулевым или отрицательным количеством"
                    )
            except ZeroQuantity as e:
                # Выводит соответствующее сообщение при вызове исключения
                print(f"Ошибка: {e}")
            else:
                # В случае успешного добавления товара выводит сообщение, что товар добавлен
                self.__products.append(product)
                Category.product_count += 1
                print("Товар добавлен успешно")
            finally:
                # При любом исходе выводит сообщение, что обработка завершена
                print("Обработка добавления товара завершена")
        else:
            raise TypeError

    @property
    def products(self) -> str:
        result = ""
        for prod in self.__products:
            result += f"{str(prod)}\n"
        return result

    @property
    def products_list(self) -> list:
        return self.__products

    def __str__(self) -> str:
        total_quantity = 0
        for prod in self.__products:
            total_quantity += prod.quantity
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def middle_price(self):
        """Подсчитывает среднюю стоимость всех товаров в категории."""
        try:
            total_cost = sum(
                product.price * product.quantity for product in self.__products
            )
            total_quantity = sum(product.quantity for product in self.__products)
            return total_cost / total_quantity

        except ZeroDivisionError:
            return 0


class ProductIterator:
    category_obj: "Category"

    def __init__(self, category_obj):
        self.products = category_obj.products_list
        self.index = 0

    def __iter__(self):
        """Возвращает итератор."""
        return self

    def __next__(self):
        if self.index < len(self.products):
            # 1. Запоминаем текущий продукт по нашему индексу
            product = self.products[self.index]
            # 2. Увеличиваем индекс для следующего шага
            self.index += 1
            # 3. Возвращаем этот продукт наружу
            return product
        else:
            raise StopIteration


class Order(BaseStorage):
    """Класс для заказа товаров."""

    __products: list
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, product: Product, quantity: int):
        super().__init__(name, description)

        if not isinstance(product, Product):
            raise TypeError("В заказе должен быть указан товар класса Product")
        try:
            # Проверяем количество заказываемого товара
            if quantity <= 0:
                raise ZeroQuantity(
                    "Заказ не может содержать 0 или меньше единиц товара"
                )
        except ZeroQuantity as e:
            # Выводит соответствующее сообщение при вызове исключения
            print(f"Ошибка оформления заказа: {e}")
            self.product = None
            self.quantity = 0
            self.total_cost = 0
        else:
            # В случае успешного добавления товара выводит сообщение, что товар добавлен
            self.product = product
            self.quantity = quantity
            self.total_cost = self.product.price * self.quantity
            print("Товар добавлен в заказ успешно")
        finally:
            # При любом исходе выводит сообщение, что обработка завершена
            print("Обработка добавления товара завершена")

        self.product = product  # Ссылка на купленный товар
        self.quantity = quantity  # Количество купленного товара
        # Автоматически вычисляем итоговую стоимость
        self.total_cost = self.product.price * self.quantity

    def __str__(self) -> str:
        if self.product is None:
            return f"Заказ '{self.name}': пустой или некорректный заказ ({self.description})"

        return (
            f"Заказ '{self.name}': {self.product.name} x {self.quantity} шт. "
            f"Итого: {self.total_cost} руб. ({self.description})"
        )
