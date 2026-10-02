import json
import os

FILENAME = "inventory.json"

# -------------------------------------------------------------------
# DATA PERSISTENCE FUNCTIONS
# -------------------------------------------------------------------

def load_inventory():
    """Load inventory from inventory.json if it exists, otherwise return initial default products."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("Error reading saved file. Starting with default inventory.")
    
    # Requirement 1: Store at least three products represented using dictionaries inside a list
    return [
        {"id": "P001", "name": "Laptop", "price": 1999.99, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.00, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 75.50, "stock": 20}
    ]


def save_inventory(inventory):
    """Save the current inventory list to inventory.json."""
    try:
        with open(FILENAME, "w") as file:
            json.dump(inventory, file, indent=4)
        print("Inventory saved successfully to inventory.json. <(^-^)>")
    except IOError as e:
        print(f"Failed to save inventory: {e}")


# -------------------------------------------------------------------
# DATA MANIPULATION FUNCTIONS
# -------------------------------------------------------------------

def display_all(inventory):
    """Display all products in the required format."""
    print("\nCurrent Inventory")
    print("-------------------------")
    if not inventory:
        print("No products in inventory.")
    else:
        for item in inventory:
            print(f"ID:{item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-------------------------")


def add_product(inventory):
    """Prompt user for details and add a new product dictionary to inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    
    # Check for duplicate ID
    for item in inventory:
        if item["id"].upper() == product_id.upper():
            print(f"Error: Product ID {product_id} already exists.")
            return

    name = input("Product Name: ").strip()
    
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid input. Price must be a number and Stock must be an integer.")
        return

    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    
    inventory.append(new_product)
    print("\nProduct added successfully! <(^-^)>")


def update_stock(inventory):
    """Update stock quantity for a given product ID."""
    print("\nUpdate Stock")
    search_id = input("Enter Product ID: ").strip()
    
    for item in inventory:
        if item["id"].upper() == search_id.upper():
            print("Product Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}\n")
            
            try:
                new_stock = int(input("New Stock Quantity: "))
                item["stock"] = new_stock
                print("\nStock quantity updated successfully! <(^-^)>")
            except ValueError:
                print("Invalid quantity entered. Stock update canceled.")
            return
            
    print("Product not found.")


def search_product(inventory):
    """Search for a product by ID and display its details."""
    print("\nSearch Product")
    search_id = input("Enter Product ID: ").strip()
    
    for item in inventory:
        if item["id"].upper() == search_id.upper():
            print("\nProduct Found")
            print("------------------------------------------------")
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("------------------------------------------------")
            return
            
    print("Product not found")


# -------------------------------------------------------------------
# MENU SYSTEM & DRIVER CODE
# -------------------------------------------------------------------

def main():
    # Requirement 3: Load inventory if file exists, else default structure
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
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
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