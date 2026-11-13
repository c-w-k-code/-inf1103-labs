from __future__ import annotations


from Product import Product
from Classes import supplier



class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, supplier, download_size):
        super().__init__(product_id, name, price, stock, supplier)
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
        return cls(data["id"], data["name"], data["price"], data["stock"], supplier, data["download_size"])