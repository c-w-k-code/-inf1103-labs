from __future__ import annotations

from typing import Any

from Product import Product
from Supplier import Supplier
from Physical_product import PhysicalProduct
from Digital_product import DigitalProduct

# Registry mapping the saved "type" identifier to the class that rebuilds it.

PRODUCT_TYPES: dict[str, type[PhysicalProduct] | type[DigitalProduct]] = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def product_from_dict(data: dict[str, Any], supplier: Supplier) -> Product:
    """Create the correct Product subclass from a saved dictionary. Supplier passed in"""
    product_type = data.get("type", "physical")
    if product_type == "physical" and "weight" not in data:
        data = {**data, "weight": 0.0}
    return PRODUCT_TYPES[product_type].from_dict(data, supplier)