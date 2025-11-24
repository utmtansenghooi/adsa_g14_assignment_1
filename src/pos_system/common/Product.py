class Product:
    """
    A class to represent a product in the POS system.

    Attributes:
        product_id (str): The unique identifier for the product.
        name (str): The name of the product.
        category (str): The category of the product.
        price (float): The price of the product.
        quantity (int): The available stock quantity of the product.
    """

    def __init__(self, product_id: str, name: str, category: str, price: float, quantity: int):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product(id={self.product_id}, name={self.name}, category={self.category}, price={self.price}, quantity={self.quantity})"