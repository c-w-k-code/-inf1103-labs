#Handles user prompt, validates integer input, or returns a 'quit' signal.
def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit'): ").strip()

    if user_input.lower() == "quit":
        return "quit"

    # Reject non-numeric strings or negative numbers
    if not user_input.isdigit():
        if user_input.startswith("-") and user_input[1:].isdigit():
            print("Error: Negative numbers are not allowed. Please enter a positive value.")
        else:
            print("Error: Invalid input. Please enter a valid whole number (e.g., 25).")
        return None

    return int(user_input)

#Calculates and returns the updated inventory total.
def process_delivery(current_total, new_value):
    return current_total + new_value

#Calculates and returns a 10% tax for a specific delivery amount.
def calculate_tax(amount):
    return amount * 0.10

# Final Audit Summary Report Generation
def generate_report(total_units, deliveries_count, failed_attempts):
    print("\n==================================")
    print("       FINAL AUDIT REPORT         ")
    print("==================================")
    print(f"Total Units Processed      : {total_units}")
    print(f"Total Deliveries Processed : {deliveries_count}")
    print(f"Failed/Rejected Entries    : {failed_attempts}")
    print("==================================")


def main():
    # 1. Initialize inventory and counters
    total_inventory = 0
    deliveries_processed = 0
    failed_entries = 0

    print("--- Modular Inventory Auditor Started ---")
    print("Enter stock quantities to add. Type 'quit' to exit.\n")

    # 2. Continuous loop
    while True:
        value = get_valid_input()

        if value == "quit":
            break

        # If input is invalid, increment failed entries counter
        if value is None:
            failed_entries += 1
            continue

        # 3. Process valid delivery value
        total_inventory = process_delivery(total_inventory, value)
        delivery_tax = calculate_tax(value)
        
        # Update successful delivery counter
        deliveries_processed += 1

        print(f"-> Delivery #{deliveries_processed} Recorded")
        print(f"   Units Added: {value}")
        print(f"   Tax (10%): {delivery_tax:.2f} units")
        print(f"   Current Total Inventory: {total_inventory}\n")

    # 4. Final Reporting
    generate_report(total_inventory, deliveries_processed, failed_entries)


if __name__ == "__main__":
    main()

