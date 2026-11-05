from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# -------------------------------------------------------------------
# UI FUNCTIONS
# -------------------------------------------------------------------
def add_product_ui(inventory):
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

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if type_choice == "1":
            weight = float(input("Weight (kg): "))
            new_product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): "))
            new_product = DigitalProduct(product_id, name, price, stock, download_size)
    except ValueError:
        print("Invalid input. Price, weight and download size must be numbers and Stock must be an integer.")
        return

    inventory.add_product(new_product)
    print("\nProduct added successfully! <(^-^)>")


def update_stock_ui(inventory):
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


def search_product_ui(inventory):
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
