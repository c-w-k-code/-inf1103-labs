from baseline_products import load_inventory, save_inventory
from ui import add_product_ui, update_stock_ui, search_product_ui, remove_product_ui, create_order_ui


def main():
    inventory = load_inventory()

    while True:
        print("\nMenu Options:")
        print("1. Display All Products 📋")
        print("2. Add Product 🛒")
        print("3. Update Stock 📦")
        print("4. Search Product 🔍")
        print("5. Remove Product 🗑️")
        print("6. Create Order 🧾")
        print("7. Save Inventory 💾")
        print("8. Save and Quit 🚪")

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