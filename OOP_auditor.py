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


# -------------------------------------------------------------------
# INVENTORY CLASS (Single Responsibility: Manage a collection of products)
# -------------------------------------------------------------------
class Inventory:
    def __init__(self):
        self._products = []

    def add_product(self, product):
        """Add a Product object to the inventory collection."""
        self._products.append(product)

    def search_product(self, product_id):
        """Search for a product by ID and return the Product object or None."""
        for product in self._products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def display_all(self):
        """Display all products in inventory."""
        print("\nCurrent Inventory")
        print("-------------------------")
        if not self._products:
            print("No products in inventory.")
        else:
            for product in self._products:
                product.display_information()
        print("-------------------------")

    @property
    def products(self):
        """Return the list of products for persistence/serialization."""
        return self._products