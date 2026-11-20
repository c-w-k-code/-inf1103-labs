from __future__ import annotations

from Inventory import Inventory
from Product_factory import ProductFactory
from Supplier import Supplier


def create_default_inventory() -> Inventory:
    """Default products used when there is no (readable) saved file.

    Each Supplier is created first, then handed to the products it supplies.
    One supplier is shared by two products.
    """
    tech_source = Supplier("S001", "TechSource Ltd", "sales@techsource.example")
    software_hub = Supplier("S002", "SoftwareHub", "licensing@softwarehub.example")

    inventory = Inventory()
    inventory.add_product(
        ProductFactory.create("physical", "P001", "Laptop", 1999.99, 15, tech_source, extra=2.2)
    )
    inventory.add_product(
        ProductFactory.create("physical", "P002", "Mouse", 25.00, 40, tech_source, extra=0.1)
    )
    inventory.add_product(
        ProductFactory.create("digital", "D001", "Antivirus Software", 49.99, 100, software_hub, extra=350.0)
    )
    return inventory