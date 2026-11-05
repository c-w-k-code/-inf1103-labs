
# -------------------------------------------------------------------
# DIGITAL PRODUCT
# -------------------------------------------------------------------
class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    @property
    def download_size(self):
        return self._download_size

    def display_information(self):
        super().display_information()
        print(f"    Download Size: {self._download_size} MB")
        print(f"    Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "This product is delivered digitally via download."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"], data["download_size"])


# Registry mapping the saved "type" identifier to the class that rebuilds it.

PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def product_from_dict(data):
    """Create the correct Product subclass from a saved dictionary."""
    product_type = data.get("type", "physical")
    if product_type == "physical" and "weight" not in data:
        data = {**data, "weight": 0.0}
    return PRODUCT_TYPES[product_type].from_dict(data)
