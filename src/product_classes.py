class Product:
    """Класс для представления сотрудника."""
    name: str
    description: str
    price: float
    quantity: int

    # Переменная на уровне класса для подсчета количества сотрудников
    number_of_product = 0

    def __init__(self, name, description, price, quantity):
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

        Product.number_of_product += 1
