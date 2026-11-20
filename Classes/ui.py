from __future__ import annotations

from DiscountStrategy import (
    BulkDiscount,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    StudentDiscount,
)
from Inventory import Inventory
from Order import Order
from Persistence import load_products
from Product_factory import ProductFactory
from Supplier import Supplier

# -------------------------------------------------------------------
# UI FUNCTIONS
# -------------------------------------------------------------------


def get_positive_float(prompt: str) -> float:
    """Prompt until the user enters a valid float greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_float(prompt: str) -> float:
    """Prompt until the user enters a valid float that is zero or more."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter zero or a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 2.5")


def get_non_negative_int(prompt: str) -> int:
    """Prompt until the user enters a whole number that is zero or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter zero or a positive whole number.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 10")


def get_positive_int(prompt: str) -> int:
    """Prompt until the user enters a whole number greater than zero."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a whole number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 3")


def get_non_empty(prompt: str) -> str:
    """Prompt until the user types something other than blank."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def get_percentage(prompt: str) -> float:
    """Prompt until the user enters a percentage between 0 and 100."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0 or value > 100:
                print("Please enter a percentage between 0 and 100.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 10")


def choose_discount_ui() -> DiscountStrategy:
    """Let the user pick a discount strategy (Strategy pattern: Order never sees the details)."""
    print("\nSelect Discount")
    print("1. No Discount")
    print("2. Percentage Discount")
    print("3. Bulk Discount (fixed amount off when total reaches a threshold)")
    print("4. Student Discount")
    while True:
        choice = input("Discount option: ").strip()
        if choice == "1":
            return NoDiscount()
        if choice == "2":
            return PercentageDiscount(get_percentage("Percentage off (0-100): "))
        if choice == "3":
            threshold = get_positive_float("Threshold total: ")
            amount = get_positive_float("Amount off: ")
            return BulkDiscount(threshold, amount)
        if choice == "4":
            return StudentDiscount()
        print("Invalid option. Please enter a number between 1 and 4.")


def _choose_supplier(inventory: Inventory) -> Supplier:
    """Reuse or create a new supplier for a product."""
    suppliers = {s.supplier_id.upper(): s for s in inventory.get_suppliers()}
    print("\nSuppliers:")
    for supplier in suppliers.values():
        supplier.display_information(indent="    ")
    supplier_id = get_non_empty("\nEnter Supplier ID (existing or new): ")

    existing = suppliers.get(supplier_id.upper())
    if existing is not None:
        return existing

    name = get_non_empty("Enter Supplier Name: ")
    contact_email = get_non_empty("Enter Supplier Contact Email: ")
    return Supplier(supplier_id, name, contact_email)


def add_product_ui(inventory: Inventory) -> None:
    """Prompt user for details and add a new physical or digital product."""
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    type_choice = input("Product type: ").strip()
    if type_choice not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = get_non_empty("Product ID: ")
    if inventory.search_product(product_id):
        print(f"Error: Product ID {product_id} already exists.")
        return

    name = get_non_empty("Product Name: ")
    supplier = _choose_supplier(inventory)

    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")
    try:
        if type_choice == "1":
            extra = get_non_negative_float("Weight (kg): ")
            new_product = ProductFactory.create("physical", product_id, name, price, stock, supplier, extra)
        else:
            extra = get_non_negative_float("Download Size (MB): ")
            new_product = ProductFactory.create("digital", product_id, name, price, stock, supplier, extra)
    except ValueError as exc:  # safety net: the Product classes still enforce their own rules
        print(f"Invalid input: {exc}")
        return

    inventory.add_product(new_product)
    print("\nProduct added successfully! <(^-^)>")


def update_stock_ui(inventory: Inventory) -> None:
    """Update stock quantity for a given product ID."""
    print("\nUpdate Stock")
    search_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(search_id)
    if product:
        print("Product Found:")
        print(f"Name: {product.name}")
        print(f"Current Stock: {product.stock}\n")

        new_stock = get_non_negative_int("New Stock Quantity: ")
        product.update_stock(new_stock)
        print("\nStock quantity updated successfully! <(^-^)>")
    else:
        print("Product not found.")


def search_product_ui(inventory: Inventory) -> None:
    """Search for a product by ID and display its details."""
    print("\nSearch Product")
    search_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(search_id)
    if product:
        print("\nProduct Found")
        print("------------------------------------------------")
        product.display_information()
        print("------------------------------------------------")
    else:
        print("Product not found")


def remove_product_ui(inventory: Inventory) -> None:
    """Remove a product from the inventory. Not destroyed."""
    print("\nRemove Product")
    search_id = input("Enter Product ID to remove: ").strip()

    removed = inventory.remove_product(search_id)
    if removed:
        print(f"Product ID {search_id} removed successfully! <(^-^)>")
        print("Note: The product is not destroyed and can be re-added later.")
    else:
        print("Product not found.")


def create_order_ui(inventory: Inventory) -> None:
    """Build a new Order; OrderLines handled by itself."""
    print("\nCreate New Order")
    order = Order(get_non_empty("Enter Order ID: "))

    while True:
        product_id = input("\nEnter Product ID to add to order (leave blank to finish): ").strip()
        if not product_id:
            break

        product = inventory.search_product(product_id)
        if product is None:
            print("Product not found.")
            continue

        quantity = get_positive_int(f"Enter quantity for {product.name}: ")
        order.add_order_line(product, quantity)

    if order.order_lines:
        order.set_discount(choose_discount_ui())
        order.display_information()
        print("\nOrders not saved")
    else:
        print("No items added. Order discarded.")


def load_products_ui(inventory: Inventory) -> None:
    """Load products from a CSV file via ProductFactory (bad rows are skipped, missing file handled)."""
    print("\nLoad Products from CSV")
    path = input("CSV file path (leave blank for products.csv): ").strip() or "products.csv"
    supplier = _choose_supplier(inventory)
    load_products(path, inventory, supplier)