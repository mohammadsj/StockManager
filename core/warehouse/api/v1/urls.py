from django.urls import path
from . import views

app_name = "api-v1"


urlpatterns = [
    path("wares/", views.WareCreateAPIView.as_view(), name="create-ware"),
    path(
        "inventory/input/",
        views.InputTransactionAPIView.as_view(),
        name="input-transaction",
    ),
    path(
        "inventory/output/",
        views.OutputTransactionAPIView.as_view(),
        name="output-transaction",
    ),
    path(
        "inventory/valuation/",
        views.InventoryValuationAPIView.as_view(),
        name="inventory-valuation",
    ),
]
