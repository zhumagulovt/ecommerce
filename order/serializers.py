from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    order_items = serializers.SerializerMethodField(read_only=True)

    def get_order_items(self, obj):
        order_items = obj.items.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data