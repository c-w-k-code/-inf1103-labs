import json
import os

FILENAME = "inventory.json"

# -------------------------------------------------------------------
# PRODUCT CLASS 
# -------------------------------------------------------------------
class Product:
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self.name = name
        self._price = price
        self._stock = stock

    @property
    def product_id(self):
        return self._product_id

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    def update_stock(self, quantity):
        """Update the stock quantity for the product securely."""
        self._stock = quantity

    def display_information(self):
        """Display single product details in the required format."""
        print(f"ID:{self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")


# -------------------------------------------------------------------
# INVENTORY CLASS 
# -------------------------------------------------------------------
class Inventory:
    def __init__(self):
        self._products = []

    def add_product(self, product):
        """Add a Product object to the inventory collection."""
        self._products.append(product)

    def search_product(self, product_id):
        """Search for a product by ID and return the Product object or None."""
        for product in self._products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def display_all(self):
        """Display all products in inventory."""
        print("\nCurrent Inventory")
        print("-------------------------")
        if not self._products:
            print("No products in inventory.")
        else:
            for product in self._products:
                product.display_information()
        print("-------------------------")

    @property
    def products(self):
        """Return the list of products for persistence/serialization."""
        return self._products


def load_inventory():
    """Load inventory from inventory.json into Product objects, otherwise return default products."""
    inventory = Inventory()
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
                for item in data:
                    product = Product(item["id"], item["name"], item["price"], item["stock"])
                    inventory.add_product(product)
                return inventory
        except (json.JSONDecodeError, IOError):
            print("Error reading saved file. Starting with default inventory.")
    
    # Default products if file doesn't exist or error occurs
    default_products = [
        Product("P001", "Laptop", 1999.99, 15),
        Product("P002", "Mouse", 25.00, 40),
        Product("P003", "Keyboard", 75.50, 20)
    ]
    for p in default_products:
        inventory.add_product(p)
    return inventory


def save_inventory(inventory):
    """Save the current inventory collection to inventory.json as dictionaries."""
    try:
        data = []
        for product in inventory.products:
            data.append({
                "id": product.product_id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            })
        with open(FILENAME, "w") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully to inventory.json. <(^-^)>")
    except IOError as e:
        print(f"Failed to save inventory: {e}")


def add_product_ui(inventory):
    """Prompt user for details and add a new Product to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    
    # Check for duplicate ID using Inventory search
    if inventory.search_product(product_id):
        print(f"Error: Product ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid input. Price must be a number and Stock must be an integer.")
        return

    new_product = Product(product_id, name, price, stock)
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
        print(f"ID: {product.product_id}")
        print(f"Name: {product.name}")
        print(f"Price: ${product.price:.2f}")
        print(f"Stock: {product.stock}")
        print("------------------------------------------------")
    else:
        print("Product not found")

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():
    inventory = load_inventory()

    while True:
        print("\nMenu Options:")
        print("1. Display All Products 📋")
        print("2. Add Product 🛒")
        print("3. Update Stock 📦")
        print("4. Search Product 🔍")
        print("5. Save Inventory 💾")
        print("6. Save and Quit 🚪")
        
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_ui(inventory)
        elif choice == "3":
            update_stock_ui(inventory)
        elif choice == "4":
            search_product_ui(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()        