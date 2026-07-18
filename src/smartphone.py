from src.product_classes import Product


class Smartphone(Product):

    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other):
        if type(other) is Smartphone:
            result_sum = self.price * self.quantity + other.price * other.quantity
            return result_sum
        raise TypeError
