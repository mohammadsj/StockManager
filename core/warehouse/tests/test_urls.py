from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..api.v1.views import (
    WareCreateAPIView,
    InputTransactionAPIView,
    OutputTransactionAPIView,
    InventoryValuationAPIView,
)


class TestUrl(SimpleTestCase):

    def test_create_ware_url_resolve(self):
        url = reverse("warehouse:api-v1:create-ware")
        self.assertEquals(resolve(url).func.view_class, WareCreateAPIView)

    def test_input_transaction_url_resolve(self):
        url = reverse("warehouse:api-v1:input-transaction")
        self.assertEquals(resolve(url).func.view_class, InputTransactionAPIView)

    def test_output_transaction_url_resolve(self):
        url = reverse("warehouse:api-v1:output-transaction")
        self.assertEquals(resolve(url).func.view_class, OutputTransactionAPIView)

    def test_inventory_valuation_url_resolve(self):
        url = reverse("warehouse:api-v1:inventory-valuation")
        self.assertEquals(resolve(url).func.view_class, InventoryValuationAPIView)
