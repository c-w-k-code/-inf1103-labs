from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from Classes import supplier
from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self.name = name
        self._price = price
        self._stock = stock
        self.supplier: Supplier = supplier 
        

    @property
    def product_id(self):
        return self._product_id

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    @property
    def supplier(self):
        return self._supplier

    def update_stock(self, quantity):
        """Update the stock quantity for the product securely."""
        self._stock = quantity

    def display_information(self):
        """Display the common product details (children extend this)."""
        print(f"ID:{self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")
        self.supplier.display_information(indent="  ")
    
    @abstractmethod
    def get_fulfilment_info(self):
        """Return a message describing how this product is fulfilled."""
        pass

    def to_dict(self):
        """Common data used for saving; subclasses add their own fields."""
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "supplier_id": self._supplier.supplier_id,
        }