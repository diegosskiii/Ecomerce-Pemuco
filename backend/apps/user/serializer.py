"""
Este módulo contiene serializadores para convertir 
objetos Python en representaciones JSON y viceversa, 
utilizados en la API REST para los modelos Region, Address y User.

Módulos externos requeridos:
    - rest_framework.serializers: Contiene las clases base para crear serializadores.

Clases de Serializadores:
- RegionSerializer: Serializador para el modelo Region.
- AddressSerializer: Serializador para el modelo Address,
     incluye la creación de una nueva región si no existe.
- UserTokenSerializer: Serializador para el modelo User, 
    utilizado para la autenticación del usuario.
- UserListSerializer: Serializador para el modelo User, 
    utilizado para listar usuarios.
- UserSerializer: Serializador para el modelo User,
    incluye la creación y actualización de la dirección del usuario.

Métodos:
- create(self, validated_data): Método utilizado para crear una nueva instancia de Address y User, 
      con la opción de crear una nueva región si no existe.
- update(self, instance, validated_data): Método utilizado para actualizar una instancia de User, 
      incluyendo la actualización de la dirección del usuario si se proporciona.

"""
from rest_framework import serializers
from .models import Region, Address, User


class RegionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Region."""
    class Meta:
        """proporcionar metadatos adicionales sobre el serializador"""
        model = Region
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Address."""
    region = RegionSerializer()
    class Meta:
        """proporcionar metadatos adicionales sobre el serializador"""
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        region_data = validated_data.pop('region')
        region_instance, created = Region.objects.get_or_create(**region_data)
        address_instance = Address.objects.create(region=region_instance, **validated_data)
        return address_instance

class UserTokenSerializer(serializers.ModelSerializer):
    """Serializador para el modelo User utilizado en la autenticación."""
    class Meta:
        """proporcionar metadatos adicionales sobre el serializador"""
        model = User
        fields = ('username', 'email', 'name')

class UserListSerializer(serializers.ModelSerializer):
    """Serializador para el modelo User utilizado para listar usuarios."""
    address = AddressSerializer()
    class Meta:
        """proporcionar metadatos adicionales sobre el serializador"""
        model = User
        fields ='__all__'

class UserSerializer(serializers.ModelSerializer):
    """Serializador para el modelo User."""
    address = AddressSerializer()

    class Meta:
        """proporcionar metadatos adicionales sobre el serializador"""
        model = User
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)
        address_instance = address_serializer.save()

        password = validated_data.pop('password')
        user_instance = User.objects.create(address=address_instance, **validated_data)

        user_instance.set_password(password)
        user_instance.save()

        return user_instance
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)

        # Actualiza los campos en User
        updated_user = super().update(instance,validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()

        # Actualiza el campo address si se proporciona
        if address_data:
            address_instance = instance.address
            region_data = address_data.pop('region', None)
            if region_data:
                region_instance, created = Region.objects.get_or_create(**region_data)
                address_instance.region = region_instance

            for key, value in address_data.items():
                setattr(address_instance, key, value)

            address_instance.save()

        instance.save()
        return instance
