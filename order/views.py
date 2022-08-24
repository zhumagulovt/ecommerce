from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from order.serializers import OrderSerializer

from products.models import Product

from .models import Order, OrderItem

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data
    order_items = data['orderItems']

    if order_items and len(order_items) == 0:
        return Response({'detail': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            total=data['totalPrice']
        )

        for i in order_items:
            product = Product.objects.get(id=i['id'])
            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=i['quantity']
            )
            product.amount -= i['quantity']
            product.sold += i['quantity']
            product.save()
            
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)