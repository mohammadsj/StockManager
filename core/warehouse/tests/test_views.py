from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from ..models import Ware, Factor


class InventoryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ware = Ware.objects.create(name="Test Ware", cost_method="fifo")
        self.input_factor = Factor.objects.create(
            ware=self.ware,
            quantity=100,
            purchase_price=10.00,
            type="input",
            total_cost=1000.00,
        )

    def test_create_ware(self):
        url = reverse("warehouse:api-v1:create-ware")
        data = {"name": "New Ware", "cost_method": "weighted_mean"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ware.objects.count(), 2)
        self.assertEqual(Ware.objects.get(id=response.data["id"]).name, "New Ware")

    def test_input_transaction(self):
        url = reverse("warehouse:api-v1:input-transaction")
        data = {"ware": self.ware.id, "quantity": 50, "purchase_price": 15.00}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Factor.objects.filter(type="input").count(), 2)
        self.assertEqual(Factor.objects.last().quantity, 50)

    def test_output_transaction_fifo(self):
        url = reverse("warehouse:api-v1:output-transaction")
        data = {"ware": self.ware.id, "quantity": 50}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Factor.objects.filter(type="output").count(), 1)
        self.assertEqual(Factor.objects.filter(type="input").count(), 1)

    def test_inventory_valuation(self):
        url = reverse("warehouse:api-v1:inventory-valuation")
        response = self.client.get(url, {"ware_id": self.ware.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity_in_stock"], 100)
        self.assertEqual(response.data["total_inventory_value"], 1000.00)
