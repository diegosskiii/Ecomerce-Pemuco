from rest_framework import serializers
from apps.cart.models import CartDetail, Cart, CartState
from apps.product.models import Product
from apps.user.models import User

class ProductQuantitySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartDetail
        fields = ['product', 'cantidad']  # Cambiado de 'quantity' a 'cantidad'

class CartDetailSerializer(serializers.ModelSerializer):
    products = ProductQuantitySerializer(many=True, write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = CartDetail
        fields = ['user', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        user = validated_data.pop('user')

        # Verificar si el usuario ya tiene un carrito
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            cart_state = CartState.objects.create(state='active')
            cart = Cart.objects.create(user=user, cart_state=cart_state)

        # Verificar si el carrito pertenece al usuario
        if cart.user != user:
            raise serializers.ValidationError("El carro no corresponde al usuario")

        cart_details = []
        for product_data in products_data:
            cart_detail = CartDetail.objects.create(cart=cart, **product_data)
            cart_details.append(cart_detail)

        return cart_details
    
    def to_representation(self, instance):
        return {
            "cart_id": instance.cart.cart_id,
            "user": instance.cart.user.username,
            "product": instance.product.product_name,
            "cantidad": instance.cantidad
        }