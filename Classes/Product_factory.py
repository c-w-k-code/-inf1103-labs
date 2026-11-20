from __future__ import annotations

from typing import Any

from Digital_product import DigitalProduct
from Physical_product import PhysicalProduct
from Product import Product
from Supplier import Supplier

# Registry mapping the saved "type" identifier to the class that rebuilds it.
PRODUCT_TYPES: dict[str, type[PhysicalProduct] | type[DigitalProduct]] = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


class ProductFactory:
    """Centralised factory for creating Product subclasses."""

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        extra: float = 0.0,
    ) -> Product:
        normalized = product_type.strip().lower()
        if normalized == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, extra)
        if normalized == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, extra)
        raise ValueError(f"Unknown product type: {product_type}")


def product_from_dict(data: dict[str, Any], supplier: Supplier) -> Product:
    """Create the correct Product subclass from a saved dictionary."""
    product_type = data.get("type", "physical")
    if product_type == "physical":
        extra = float(data.get("weight", 0.0))
    elif product_type == "digital":
        extra = float(data.get("download_size", 0.0))
    else:
        raise ValueError(f"Unknown product type: {product_type}")

    return ProductFactory.create(
        product_type=product_type,
        product_id=data["id"],
        name=data["name"],
        price=data["price"],
        stock_quantity=data["stock"],
        supplier=supplier,
        extra=extra,
    )