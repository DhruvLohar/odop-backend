from rest_framework import serializers
from .models import Order, OrderLineItem

from product.serializers import ProductSerializer
from user.serializers import UserSerializer

class OrderLineItemSerializer(serializers.ModelSerializer):
    
    product = ProductSerializer()
    
    class Meta:
        model = OrderLineItem
        fields = ['id', 'product', 'buying_quantity', 'status', 'estimate_delivery_time', 'subtotal', 'total']

class ArtisanOrdersListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderLineItem
        fields = '__all__'
    
    def get_order(self, instance: OrderLineItem):
        return dict(
            shipping_address=instance.order.shipping_address,
            payment_mode=instance.order.payment_mode
        )

class OrderSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    related_line_items = OrderLineItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'shipping_address', 'created_at', 'modified_at', 'related_line_items']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'shipping_address', 'payment_mode']
        
    def create(self, validated_data):
        order = super().create(validated_data)
        
        order_lines = self.context.pop('order_lines')
        
        for orderLine in order_lines:
            orderLine["order"] = order.id
            
            orderline_serializer = OrderLineItemCreateSerializer(data=orderLine)
            orderline_serializer.is_valid(raise_exception=True)
            orderline_serializer.save()
                
        return order

class OrderLineItemCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderLineItem
        fields = ['order', 'product', 'buying_quantity']
        
    def create(self, validated_data):
        
        orderLineItem = super().create(validated_data)
        orderLineItem.calculateCosting()
        orderLineItem.save()
        
        return orderLineItem