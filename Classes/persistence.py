from __future__ import annotations

import csv
import json
import os
from typing import Any

from Baseline_products import create_default_inventory
from Inventory import Inventory
from Product_factory import ProductFactory, product_from_dict
from Supplier import Supplier

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
    """Load inventory from inventory.json, otherwise return default products.

    ValueError covers both bad JSON (JSONDecodeError is a ValueError) and saved
    values that break validation rules, e.g. a price of 0 or negative stock.
    """
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r", encoding="utf-8") as file:
                data = json.load(file)
            return _build_inventory(data)
        except (ValueError, OSError, KeyError, TypeError):
            print("Error reading saved file. Starting with default inventory.")
    return create_default_inventory()


def save_inventory(inventory: Inventory) -> None:
    """Save suppliers and products to inventory.json (each object describes itself)."""
    try:
        data = {
            "suppliers": [s.to_dict() for s in inventory.get_suppliers()],
            "products": [p.to_dict() for p in inventory.products],
        }
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully to inventory.json. <(^-^)>")
    except OSError as e:
        print(f"Failed to save inventory: {e}")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file into inventory via ProductFactory."""
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            header = next(reader, None)
            if header is not None:
                for row_num, row in enumerate(reader, start=2):
                    if not row:
                        continue
                    try:
                        if len(row) < 5:
                            raise ValueError("Missing required columns.")
                        product_type = row[0].strip()
                        product_id = row[1].strip()
                        name = row[2].strip()
                        price = float(row[3].strip())
                        stock_quantity = int(row[4].strip())
                        extra = float(row[5].strip()) if len(row) >= 6 and row[5].strip() else 0.0
                        product = ProductFactory.create(
                            product_type=product_type,
                            product_id=product_id,
                            name=name,
                            price=price,
                            stock_quantity=stock_quantity,
                            supplier=supplier,
                            extra=extra,
                        )
                        inventory.add_product(product)
                        loaded += 1
                    except ValueError as exc:
                        print(f"Skipping invalid row {row_num} ({row}): {exc}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")