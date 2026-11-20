from __future__ import annotations

from DiscountStrategy import DiscountStrategy, NoDiscount
from Order_line import OrderLine
from Product import Product


class Order:
    """An order containing OrderLines (composition) and a DiscountStrategy (association)."""

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self._order_id: str = order_id
        self._order_lines: list[OrderLine] = []
        self._discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return list(self._order_lines)

    @property
    def discount(self) -> DiscountStrategy:
        return self._discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Replace the active discount strategy on this order."""
        self._discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Created internally, added to this order."""
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
        """Calculate the total cost of the order using the configured strategy."""
        total: float = sum(line.calculate_subtotal() for line in self._order_lines)
        return self._discount.apply(total)

    def display_information(self) -> None:
        print(f"\nOrder ID: {self._order_id}")
        print("-------------------------")
        for order_line in self._order_lines:
            order_line.display_information()
        print(f"Total Order Cost: ${self.calculate_total():.2f}")
        print("-------------------------")