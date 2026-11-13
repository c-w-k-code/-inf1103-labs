from __future__ import annotations

import json
import os
from typing import Any

from Inventory import Inventory
from Supplier import Supplier
from Product_factory import product_from_dict
from Baseline_products import create_default_inventory

# -------------------------------------------------------------------
# PERSISTENCE
# -------------------------------------------------------------------
FILENAME: str = "inventory.json"
 
 
def _build_inventory(data: list[dict[str, Any]] | dict[str, Any]) -> Inventory:
    """Turn loaded JSON into an Inventory of Product objects."""
    inventory = Inventory()
    if isinstance(data, list):
        unknown = Supplier("S000", "Unknown Supplier", "unknown@example.com")
        for item in data:
            inventory.add_product(product_from_dict(item, unknown))
    else:
        suppliers = {s["id"]: Supplier.from_dict(s) for s in data["suppliers"]}
        for item in data["products"]:
            inventory.add_product(product_from_dict(item, suppliers[item["supplier_id"]]))
    return inventory
 
 
def load_inventory() -> Inventory:
    """Load inventory from inventory.json, otherwise return default products."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
            return _build_inventory(data)
        except (json.JSONDecodeError, IOError, KeyError, TypeError):
            print("Error reading saved file. Starting with default inventory.")
    return create_default_inventory()
 
 
def save_inventory(inventory: Inventory) -> None:
    """Save suppliers and products to inventory.json (each object describes itself)."""
    try:
        data = {
            "suppliers": [s.to_dict() for s in inventory.get_suppliers()],
            "products": [p.to_dict() for p in inventory.products],
        }
        with open(FILENAME, "w") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully to inventory.json. <(^-^)>")
    except IOError as e:
        print(f"Failed to save inventory: {e}")

