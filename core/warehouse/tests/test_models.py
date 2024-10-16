from django.test import TestCase
from ..models import Ware, Factor


class WareFactorModelTest(TestCase):

    def setUp(self):
        self.ware = Ware.objects.create(name="Test Ware", cost_method="fifo")

    def test_create_ware(self):
        ware_count = Ware.objects.count()
        self.assertEqual(ware_count, 1)
        self.assertEqual(self.ware.name, "Test Ware")
        self.assertEqual(self.ware.cost_method, "fifo")

    def test_create_factor_input(self):
        factor = Factor.objects.create(
            ware=self.ware,
            quantity=100,
            purchase_price=50.00,
            total_cost=5000.00,
            type="input",
        )

        factor_count = Factor.objects.count()
        self.assertEqual(factor_count, 1)
        self.assertEqual(factor.ware, self.ware)
        self.assertEqual(factor.quantity, 100)
        self.assertEqual(factor.purchase_price, 50.00)
        self.assertEqual(factor.total_cost, 5000.00)
        self.assertEqual(factor.type, "input")

    def test_create_factor_output(self):
        factor = Factor.objects.create(
            ware=self.ware,
            quantity=50,
            purchase_price=40.00,
            total_cost=2000.00,
            type="output",
        )

        factor_count = Factor.objects.count()
        self.assertEqual(factor_count, 1)
        self.assertEqual(factor.ware, self.ware)
        self.assertEqual(factor.quantity, 50)
        self.assertEqual(factor.purchase_price, 40.00)
        self.assertEqual(factor.total_cost, 2000.00)
        self.assertEqual(factor.type, "output")
