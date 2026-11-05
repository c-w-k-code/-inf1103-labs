
# -------------------------------------------------------------------
# PERSISTENCE
# -------------------------------------------------------------------
def load_inventory():
    """Load inventory from inventory.json, otherwise return default products."""
    inventory = Inventory()
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
            for item in data:
                inventory.add_product(product_from_dict(item))
            return inventory
        except (json.JSONDecodeError, IOError, KeyError):
            print("Error reading saved file. Starting with default inventory.")
            inventory = Inventory()

    default_products = [
        PhysicalProduct("P001", "Laptop", 1999.99, 15, 2.2),
        PhysicalProduct("P002", "Mouse", 25.00, 40, 0.1),
        DigitalProduct("D001", "Antivirus Software", 49.99, 100, 350.0),
    ]
    for p in default_products:
        inventory.add_product(p)
    return inventory


def save_inventory(inventory):
    """Save the inventory to inventory.json (each product describes itself)."""
    try:
        data = [product.to_dict() for product in inventory.products]
        with open(FILENAME, "w") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully to inventory.json. <(^-^)>")
    except IOError as e:
        print(f"Failed to save inventory: {e}")

