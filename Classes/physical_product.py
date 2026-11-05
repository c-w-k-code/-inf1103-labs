from Product import Product
from CanBeShipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """Single class inheritance (Product) + one interface (CanBeShipped)."""

    BASE_SHIPPING = 5.00
    COST_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    def display_information(self):
        super().display_information()
        print(f"    Weight: {self._weight} kg")
        print(f"    Fulfilment: {self.get_fulfilment_info()}")
        print(f"    Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        """Simple rule: base fee + a fixed rate per kg."""
        return self.BASE_SHIPPING + self.COST_PER_KG * self._weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"], data["weight"])