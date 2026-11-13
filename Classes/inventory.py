from __future__ import annotations

from Product import Product
from Supplier import Supplier


# -------------------------------------------------------------------
# INVENTORY CLASS
# -------------------------------------------------------------------
class Inventory:
    def __init__(self) -> None:
        self._products: list[Product] = []

    def add_product(self, product: Product) -> None:
        """Add a Product object to the inventory collection."""
        self._products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Remove a product from the inventory by its ID."""
        product = self.search_product(product_id)
        if product is not None:
            self._products.remove(product)
        return product

    def search_product(self, product_id: str) -> Product | None:
        """Search for a product by ID and return the Product object or None."""
        for product in self._products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def display_all(self) -> None:
        """Display all products in inventory."""
        print("\nCurrent Inventory")
        print("-------------------------")
        if not self._products:
            print("No products in inventory.")
        else:
            for product in self._products:
                product.display_information()
        print("-------------------------")

    def get_suppliers(self) -> list[Supplier]:
        """Return a list of all unique suppliers in the inventory."""
        suppliers:dict[str, Supplier] = {}
        for product in self._products:
            suppliers.setdefault(product.supplier.supplier_id, product.supplier)
        return list(suppliers.values())

    @property
    def products(self) -> list[Product]:
        """Return the list of products for persistence/serialization."""
        return self._products