from __future__ import annotations

import io
import os
import tempfile
import unittest
from unittest.mock import patch

from DiscountStrategy import BulkDiscount, NoDiscount, PercentageDiscount, StudentDiscount
from Inventory import Inventory
from Order import Order
from Persistence import load_products
from Product import Product
from Product_factory import ProductFactory
from Supplier import Supplier
from DiscountStrategy import DiscountStrategy
from Order_line import OrderLine
from Physical_product import PhysicalProduct
from Ui import get_non_negative_int, get_positive_float, get_positive_int


class TestLab09DesignAndErrorHandling(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.product = ProductFactory.create(
            "physical", "P001", "Desk Lamp", 50.0, 10, self.supplier, 1.5
        )

    def test_order_uses_discount_strategy_and_set_discount(self) -> None:
        order = Order("O001")
        order.add_order_line(self.product, 5)  # subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 250.0)

        order.set_discount(BulkDiscount(200.0, 20.0))
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10.0))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_without_modifying_order(self) -> None:
        order = Order("O002", discount=StudentDiscount(5.0))
        order.add_order_line(self.product, 2)  # subtotal = 100.0 -> 95.0
        self.assertAlmostEqual(order.calculate_total(), 95.0)

    def test_product_factory_creates_product_and_rejects_unknown_type(self) -> None:
        digital = ProductFactory.create(
            "digital", "D001", "E-Book", 15.0, 20, self.supplier, 12.5
        )
        self.assertIsInstance(digital, Product)
        self.assertEqual(digital.product_id, "D001")

        with self.assertRaises(ValueError):
            ProductFactory.create("service", "S001", "Install", 30.0, 5, self.supplier)

    def test_validation_rules(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P002", "Bad Price", 0.0, 5, self.supplier)

        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P003", "Neg Stock", 10.0, -1, self.supplier)

        with self.assertRaises(ValueError):
            self.product.update_stock(-3)

        order = Order("O003", discount=NoDiscount())
        with self.assertRaises(ValueError):
            order.add_order_line(self.product, 0)

    def test_get_positive_float_retries_on_bad_input(self) -> None:
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = get_positive_float("Price: ")
        self.assertAlmostEqual(result, 12.5)

    def test_load_products_skips_bad_rows_and_handles_missing_file(self) -> None:
        inventory = Inventory()
        missing_path = os.path.join(tempfile.gettempdir(), "nonexistent_lab09_products.csv")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            load_products(missing_path, inventory, self.supplier)
        self.assertIn("Products file not found", out.getvalue())
        self.assertIn("Load attempt finished.", out.getvalue())

        csv_content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            inv2 = Inventory()
            with patch("sys.stdout", new_callable=io.StringIO) as out2:
                load_products(tmp_path, inv2, self.supplier)
            self.assertEqual(len(inv2.products), 3)
            self.assertIn("3 products loaded.", out2.getvalue())
            self.assertIn("Load attempt finished.", out2.getvalue())
        finally:
            os.remove(tmp_path)

    def test_custom_strategy_works_without_modifying_order(self) -> None:
        class FlatTenOff(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total - 10

        order = Order("O004", discount=FlatTenOff())
        order.add_order_line(self.product, 2)  # 100 -> 90
        self.assertAlmostEqual(order.calculate_total(), 90.0)

    def test_factory_returns_product_subclasses(self) -> None:
        self.assertIsInstance(self.product, PhysicalProduct)
        self.assertIsInstance(self.product, Product)

    def test_unknown_type_message_is_clear(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "S9", "X", 1.0, 1, self.supplier)

    def test_order_line_rejects_bad_quantity(self) -> None:
        with self.assertRaises(ValueError):
            OrderLine(self.product, -2)

    def test_int_helpers_retry_on_bad_input(self) -> None:
        with patch("builtins.input", side_effect=["x", "-1", "2.5", "7"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(get_non_negative_int("Stock: "), 7)
        with patch("builtins.input", side_effect=["0", "abc", "3"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(get_positive_int("Qty: "), 3)

    def test_load_products_with_lab_sheet_csv(self) -> None:
        inventory = Inventory()
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            load_products("products.csv", inventory, self.supplier)
        self.assertEqual(len(inventory.products), 3)
        self.assertIn("3 products loaded.", out.getvalue())


if __name__ == "__main__":
    unittest.main()