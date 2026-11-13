from __future__ import annotations
from typing import Any


from Product import Product
from Supplier import Supplier



class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size = download_size

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Download Size: {self._download_size} MB")
        print(f"    Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via download."

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"], Supplier.from_dict(data["supplier"]), data["download_size"])