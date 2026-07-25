class ZeroQuantity(Exception):

    def __init__(self, messages=None):
        super().__init__(messages)
