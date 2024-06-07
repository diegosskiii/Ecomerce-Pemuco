from rest_framework import serializers
from apps.cart.models import Cart, Cart_detail, Cart_state

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        