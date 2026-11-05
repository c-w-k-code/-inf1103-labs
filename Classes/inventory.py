
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