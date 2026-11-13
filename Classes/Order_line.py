from __future__ import annotations

from Product import Product

class OrderLine:
    """One product and its quantity in an order.
    
    Product (assosciation). Created and managed by order (composition)"""
    
    def __init__(self, product: Product, quantity: int) -> None:
        self._product: Product = product
        self._quantity: int = quantity

    @property
    def product(self) -> Product:
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_information(self) -> None:
        print(f" {self._product.product_id} | {self.product.name} | Quantity: {self.quantity} | Subtotal: ${self.calculate_subtotal():.2f}")