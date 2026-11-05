# -------------------------------------------------------------------
# INTERFACE
# -------------------------------------------------------------------
class CanBeShipped(ABC):
    """Contract for anything that can be shipped. No attributes, no implementation."""

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this object."""
        pass
