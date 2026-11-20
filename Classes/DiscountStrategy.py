from __future__ import annotations

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract strategy for applying a discount to an order total."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the discounted total given an order total."""
        pass


class NoDiscount(DiscountStrategy):
    """Strategy that leaves the order total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Strategy that subtracts a given percentage from the order total."""

    def __init__(self, percentage: float) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self._percentage = percentage

    @property
    def percentage(self) -> float:
        return self._percentage

    def apply(self, total: float) -> float:
        return total * (1 - self._percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Strategy that deducts a fixed amount when total meets or exceeds threshold."""

    def __init__(self, threshold: float, discount_amount: float) -> None:
        self._threshold = threshold
        self._discount_amount = discount_amount

    def apply(self, total: float) -> float:
        if total >= self._threshold:
            return max(0.0, total - self._discount_amount)
        return total


class StudentDiscount(DiscountStrategy):
    """Fourth strategy (Section 2.4): flat percentage discount for students."""

    def __init__(self, percentage: float = 5.0) -> None:
        self._percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self._percentage / 100)