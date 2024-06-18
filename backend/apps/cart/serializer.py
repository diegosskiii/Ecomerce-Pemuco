from rest_framework import serializers
from apps.cart.models import Cart, Cart_detail, Cart_state
from apps.product.models import Product
from apps.user.models import User

class CartStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_state
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CartSerializer(serializers.ModelSerializer):
    cart_state = CartStateSerializer()
    user = UserSerializer()

    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        cart_state_data = validated_data.pop('cart_state')
        user_data = validated_data.pop('user')
        cart_state_instance = Cart_state.objects.create(**cart_state_data)
        user_instance = User.objects.create(**user_data)
        cart_instance = Cart.objects.create(cart_state=cart_state_instance, user=user_instance, **validated_data)
        return cart_instance


class ProductQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_detail
        fields = ['product', 'cantidad']

class CartDetailSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    products = ProductQuantitySerializer(many=True, write_only=True)

    class Meta:
        model = Cart_detail
        fields = '__all__'
        extra_kwargs = {
            'cart': {'read_only': True}
        }
        
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        cart_data = validated_data.pop('cart')
        
        cart_serializer = CartSerializer(data=cart_data)
        cart_serializer.is_valid(raise_exception=True)
        cart_instance = cart_serializer.save()
        
        cart_detail_instances = []
        for product_data in products_data:
            product = Product.objects.get(pk=product_data['product'].id)
            cart_detail_instance = Cart_detail.objects.create(cart=cart_instance, product=product, cantidad=product_data['cantidad'])
            cart_detail_instances.append(cart_detail_instance)
        
        return cart_detail_instances