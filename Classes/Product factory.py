from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# Registry mapping the saved "type" identifier to the class that rebuilds it.

PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def product_from_dict(data):
    """Create the correct Product subclass from a saved dictionary."""
    product_type = data.get("type", "physical")
    if product_type == "physical" and "weight" not in data:
        data = {**data, "weight": 0.0}
    return PRODUCT_TYPES[product_type].from_dict(data)