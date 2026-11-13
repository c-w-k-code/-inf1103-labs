from __future__ import annotations

from Inventory import Inventory
from Order import Order
from Supplier import Supplier
from Physical_product import PhysicalProduct
from Digital_product import DigitalProduct

# -------------------------------------------------------------------
# UI FUNCTIONS
# -------------------------------------------------------------------

def _choose_supplier(inventory: Inventory) -> Supplier:
    """Reuse or create a new supplier for a product."""
    suppliers = {s.supplier_id.upper(): s for s in inventory.get_suppliers()}
    print("\nSuppliers:")
    for supplier in suppliers.values():
        supplier.display_information(indent="    ")
    supplier_id = input("\nEnter Supplier ID (existing or new): ").strip()

    existing = suppliers.get(supplier_id.upper())
    if existing is not None:
        return existing

    name = input("Enter Supplier Name: ").strip()
    contact_email = input("Enter Supplier Contact Email: ").strip()
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

    product_id = input("Product ID: ").strip()
    if inventory.search_product(product_id):
        print(f"Error: Product ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    supplier = _choose_supplier(inventory)

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if type_choice == "1":
            weight = float(input("Weight (kg): "))
            new_product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
        else:
            download_size = float(input("Download Size (MB): "))
            new_product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
    except ValueError:
        print("Invalid input. Price, weight and download size must be numbers and Stock must be an integer.")
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

        try:
            new_stock = int(input("New Stock Quantity: "))
            product.update_stock(new_stock)
            print("\nStock quantity updated successfully! <(^-^)>")
        except ValueError:
            print("Invalid quantity entered. Stock update canceled. :(")
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
    """Build a new Order; OrderLines handled by itself"""
    print("\nCreate New Order")
    order = Order(input("Enter Order ID: ").strip())

    while True:
        product_id = input("\nEnter Product ID to add to order (leave blank to finish): ").strip()
        if not product_id:
            break

        product = inventory.search_product(product_id)
        if product is None:
            print("Product not found.")
            continue

        try:
            quantity = int(input(f"Enter quantity for {product.name}: "))
        except ValueError:
            print("Invalid quantity.")
            continue
        order.add_order_line(product, quantity)

    if order.order_lines:
        order.display_information()
        print("\nOrders not saved")
    else:
        print("No items added. Order discarded.")