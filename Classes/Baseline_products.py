from __future__ import annotations

from Inventory import Inventory
from Supplier import Supplier
from Physical_product import PhysicalProduct
from Digital_product import DigitalProduct



def create_default_inventory() -> Inventory:
    """Default products used when there is no (readable) saved file.
 
    Each Supplier is created first, then handed to the products it supplies.
    One supplier is shared by two products.
    """
    tech_source = Supplier("S001", "TechSource Ltd", "sales@techsource.example")
    software_hub = Supplier("S002", "SoftwareHub", "licensing@softwarehub.example")
 
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1999.99, 15, tech_source, 2.2))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.00, 40, tech_source, 0.1))
    inventory.add_product(DigitalProduct("D001", "Antivirus Software", 49.99, 100, software_hub, 350.0))
    return inventory