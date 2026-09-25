import os

FILENAME = "inventory.txt"


def load_inventory():
    """
    Reads previously saved orders from inventory.txt.
    Returns a history list of tuples: (order_id, product_name, quantity)
    """
    history = []
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts) == 3:
                            order_id = int(parts[0].strip())
                            product_name = parts[1].strip()
                            quantity = int(parts[2].strip())
                            history.append((order_id, product_name, quantity))
        except Exception:
            pass  # If file doesn't exist or error occurs, start with an empty history
    return history


def save_inventory(history):
    """
    Saves the current transaction history list to inventory.txt and prints confirmation.
    """
    try:
        with open(FILENAME, "w") as f:
            for order_id, product, qty in history:
                f.write(f"{order_id}, {product}, {qty}\n")
        print(f"\nOrder successfully saved to {FILENAME}")
    except Exception as e:
        print(f"Error saving to file: {e}")


def get_valid_input():
    """
    Handles prompt for product details, validates integer quantity input,
    or returns a 'quit' signal.
    """
    product_name = input("Enter Product Name: ").strip()
    if product_name.lower() == "quit":
        return "quit", None

    quantity_input = input("Enter Quantity: ").strip()
    if quantity_input.lower() == "quit":
        return "quit", None

    # Validate numeric entry
    if not quantity_input.isdigit():
        if quantity_input.startswith("-") and quantity_input[1:].isdigit():
            print("Error: Negative numbers are not allowed. Please enter a positive value.\n")
        else:
            print("Error: Invalid input. Please enter a valid whole number (e.g., 25).\n")
        return None, None

    return product_name, int(quantity_input)


def process_delivery(current_total, new_value):
    """Calculates and returns the updated inventory total."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates and returns a 10% tax for a specific delivery amount."""
    return amount * 0.10


def generate_report(total_units, deliveries_count, failed_attempts):
    """Generates the final audit summary report."""
    print("\n==================================")
    print("       FINAL AUDIT REPORT         ")
    print("==================================")
    print(f"Total Units Processed      : {total_units}")
    print(f"Total Deliveries Processed : {deliveries_count}")
    print(f"Failed/Rejected Entries    : {failed_attempts}")
    print("==================================")


def main():
    # 1. Load history and calculate starting metrics
    history = load_inventory()
    total_inventory = sum(item[2] for item in history)
    deliveries_processed = len(history)
    failed_entries = 0

    # Display current orders loaded from inventory.txt
    print("Current Orders from previous entries:\n")
    if history:
        for order_id, product, qty in history:
            print(f"{order_id}, {product}, {qty}")
    print()

    # Dynamic starting ID based on order history
    next_id = 1001 + len(history)

    # 2. Main execution loop
    while True:
        product_name, quantity = get_valid_input()

        if product_name == "quit":
            break

        # Handle invalid/failed entries
        if product_name is None:
            failed_entries += 1
            continue

        # Update history and calculations
        history.append((next_id, product_name, quantity))
        total_inventory = process_delivery(total_inventory, quantity)
        delivery_tax = calculate_tax(quantity)
        deliveries_processed += 1

        # Print item add output
        print("\nNew Order Added:")
        print(f"{next_id}, {product_name}, {quantity}")

        # Save to file immediately and show confirmation
        save_inventory(history)
        print()

        next_id += 1

    # 3. Final report on exit
    generate_report(total_inventory, deliveries_processed, failed_entries)


if __name__ == "__main__":
    main()