from __future__ import annotations


class Supplier:
    def __init__(self, supplier_id:str, name:str, contact_email:str):
        self._supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    @property
    def supplier_id(self) -> str:
        return self._supplier_id

    def display_information(self, indent:str = ""):
        """Display the supplier details."""
        print(f"{indent}Supplier ID: {self._supplier_id}")
        print(f"{indent}Name: {self.name}")
        print(f"{indent}Email: {self.contact_email}")

    def to_dict(self) -> dict[str, str]:
        """Data for saving."""
        return {
            "supplier_id": self._supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]):
        """Create a Supplier instance from a dictionary."""
        return cls(
            supplier_id=data["supplier_id"],
            name=data["name"],
            contact_email=data["contact_email"]
        )