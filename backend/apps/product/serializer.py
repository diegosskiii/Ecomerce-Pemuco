from rest_framework import serializers
from apps.product.models import Product,Category,Opinion

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('state',)

    def create(self, validated_data):
        category_name = validated_data.get('category_name')
        existing_category = Category.objects.filter(category_name = category_name).first()
        if existing_category:
            raise serializers.ValidationError("The category already exists")
        return Category.objects.create(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        exclude = ('state',)

    def to_representation(self, instance):
        return {
            "product_id":instance.product_id,
            "product_name":instance.product_name,
            "price": instance.price,
            "description": instance.description,
            "stock": instance.stock,
            "category": instance.category.category_name,
            "image": instance.image.url if instance.image else None
        }
    


    '''
    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_instance, created = Category.objects.get_or_create(**category_data)
        category_instance = Category.objects.create(category=category_instance, **validated_data)
        return category_instance
    '''
    
    
