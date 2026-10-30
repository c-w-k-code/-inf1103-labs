import json
import os

FILENAME = "inventory.json"

# -------------------------------------------------------------------
# PRODUCT CLASS (Single Responsibility: Represent and manage a product)
# -------------------------------------------------------------------
class Product:
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self.name = name
        self._price = price
        self._stock = stock

    @property
    def product_id(self):
        return self._product_id

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    def update_stock(self, quantity):
        """Update the stock quantity for the product securely."""
        self._stock = quantity

    def display_information(self):
        """Display single product details in the required format."""
        print(f"ID:{self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")

