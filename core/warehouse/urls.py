from django.urls import path, include

app_name = "warehouse"

urlpatterns = [path("api/v1/", include("warehouse.api.v1.urls"))]
