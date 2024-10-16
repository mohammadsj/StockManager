from rest_framework import serializers
from ...models import Ware, Factor


class WareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ware
        fields = ["id", "name", "cost_method"]


class InputTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = (
            "id",
            "ware",
            "quantity",
            "purchase_price",
            "type",
            "created_at",
            "total_cost",
        )
        read_only_fields = ["type", "total_cost"]

    def create(self, validated_data):
        validated_data["type"] = "input"
        validated_data["total_cost"] = (
            validated_data["quantity"] * validated_data["purchase_price"]
        )
        return super().create(validated_data)


class OutputTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = ("id", "ware", "quantity", "purchase_price", "type", "total_cost")
        read_only_fields = ["type", "total_cost", "purchase_price"]
