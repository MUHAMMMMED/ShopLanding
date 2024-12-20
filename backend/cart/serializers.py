from rest_framework import serializers
from .models import *
from content.serializers import ProductSerializer
from decimal import Decimal
# from .models import *
from products.serializers import *


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields ="__all__"
 
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    notes = NoteSerializer(many=True)
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'notes', 'discount_price']

    def get_discount_price(self, obj):
        price = obj.product.price
        discount = obj.product.discount
        discount_price = price - (price * Decimal(discount) / Decimal(100))
        return discount_price
 
class CartItem_Serializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
 
class CartSerializer(serializers.ModelSerializer):
    items = CartItem_Serializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'session_id', 'created_at',  ]
 
class Cart_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields ="__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields ="__all__"


        






 