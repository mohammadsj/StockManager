from rest_framework import generics
from rest_framework.views import APIView
from ...models import Ware, Factor
from .serializers import (
    WareSerializer,
    InputTransactionSerializer,
    OutputTransactionSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class WareCreateAPIView(generics.CreateAPIView):
    queryset = Ware.objects.all()
    serializer_class = WareSerializer


class InputTransactionAPIView(generics.CreateAPIView):
    queryset = Factor.objects.filter(type="input")
    serializer_class = InputTransactionSerializer


class OutputTransactionAPIView(generics.CreateAPIView):
    serializer_class = OutputTransactionSerializer

    def post(self, request, *args, **kwargs):
        ware_id = request.data.get("ware")
        quantity_requested = int(request.data.get("quantity"))
        ware = get_object_or_404(Ware, id=ware_id)
        inputs = Factor.objects.filter(ware=ware, type="input").order_by("id")

        total_stock = sum(factor.quantity for factor in inputs)
        if quantity_requested > total_stock:
            return Response(
                {"message": "Insufficient inventory"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if ware.cost_method == "fifo":
            total_cost = self._apply_fifo(inputs, quantity_requested)
        else:  # weighted_mean
            total_cost = self._apply_weighted_mean(ware, quantity_requested)

        output = Factor.objects.create(
            ware=ware,
            quantity=quantity_requested,
            purchase_price=total_cost / quantity_requested,
            total_cost=total_cost,
            type="output",
        )
        data = {
            "factor_id": output.id,
            "ware_id": output.ware.id,
            "quantity": output.quantity,
            "total_cost": output.total_cost,
            "created_at": output.created_at,
            "type": output.type,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def _apply_fifo(self, inputs, quantity_requested):
        total_cost = 0
        for factor in inputs:
            if factor.quantity <= quantity_requested:
                quantity_requested -= factor.quantity
                total_cost += factor.purchase_price * factor.quantity
                factor.delete()
            else:
                total_cost += factor.purchase_price * quantity_requested
                factor.quantity -= quantity_requested
                factor.save()
                break
        return total_cost

    def _apply_weighted_mean(self, ware, quantity_requested):
        inputs = Factor.objects.filter(ware=ware, type="input")
        total_stock = sum(factor.quantity for factor in inputs)
        total_cost = sum(factor.total_cost for factor in inputs)
        average_price = total_cost / total_stock if total_stock else 0
        return average_price * quantity_requested


class InventoryValuationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        ware_id = request.query_params.get("ware_id")
        ware = get_object_or_404(Ware, id=ware_id)
        factors = Factor.objects.filter(ware=ware, type="input")

        total_value = sum(factor.total_cost for factor in factors)
        total_quantity = sum(factor.quantity for factor in factors)

        return Response(
            {
                "ware_id": ware.id,
                "quantity_in_stock": total_quantity,
                "total_inventory_value": total_value,
            },
            status=status.HTTP_200_OK,
        )
