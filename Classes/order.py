from __future__ import annotations

from Product import Product
from Order_line import OrderLine

class Order:
    """An order containing OrderLines(composition)."""

    def __init__(self, order_id: str) -> None:
        self._order_id: str = order_id
        self._order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return list(self._order_lines) 

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Created internally, added to this order"""
        order_line = OrderLine(product, quantity)
        self._order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """True if order line was removed."""
        for order_line in self._order_lines:
            if order_line.product.product_id.upper() == product_id.upper():
                self._order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        """Calculate the total cost of the order."""
        total: float = 0.0
        for order_line in self._order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print(f"\nOrder ID: {self._order_id}")
        print("-------------------------")
        for order_line in self._order_lines:
            order_line.display_information()
        print(f"Total Order Cost: ${self.calculate_total():.2f}")
        print("-------------------------")