from __future__ import annotations

from typing import Any

from Product import Product
from CanBeShipped import CanBeShipped
from Supplier import Supplier



class PhysicalProduct(Product, CanBeShipped):
    """Single class inheritance (Product) + one interface (CanBeShipped)."""

    BASE_SHIPPING = 5.00
    COST_PER_KG = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        super().display_information()
        print(f"    Weight: {self._weight} kg")
        print(f"    Fulfilment: {self.get_fulfilment_info()}")
        print(f"    Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Simple rule: base fee + a fixed rate per kg."""
        return self.BASE_SHIPPING + self.COST_PER_KG * self._weight

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"], Supplier, data["weight"])