"""
Este módulo proporciona vistas y funciones para gestionar usuarios mediante la API REST.

Módulos externos requeridos:
    - rest_framework.authtoken.views: Contiene vistas para la autenticación de tokens.
    - rest_framework.response: Contiene clases de respuesta HTTP para la API REST.
    - rest_framework.authtoken.models: Contiene el modelo de token de autenticación.
    - rest_framework.status: Contiene códigos de estado HTTP.
    - rest_framework.decorators: Contiene decoradores para vistas basadas en funciones.
    - .serializer: Módulo local que contiene los serializadores para los modelos de usuario.
    - .models: Módulo local que contiene los modelos de usuario.

Clases:
    Login: Vista para la autenticación de usuarios y generación de tokens.

Funciones:
    - user_api_view: Función de vista para mostrar y agregar usuarios.
    - user_detail_view: Función de vista para ver, actualizar y eliminar un usuario específico.
"""
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view
from .serializer import UserSerializer, UserListSerializer, UserTokenSerializer
from .models import User


#LOGIN
class Login(ObtainAuthToken):
    """La clase Login obtiene y sobreescribe el token del usuario."""
    def post(self,request,*args,**kwargs):
        print(request.user)
        login_serializer = self.serializer_class(data = request.data,
                                                  context = {'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token':token.key,
                        'user' : user_serializer.data
                    }, status= status.HTTP_201_CREATED)
                
                token.delete()
                token = Token.objects.create(user = user)
                return Response({
                    'token':token.key,
                    'user' : user_serializer.data
                }, status= status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Este usuario no puede iniciar sesión'},
                                 status= status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre de usuario o contraseña incorrecta'},
                             status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def user_api_view(request):
    """La funcion user_api_view permite mostrar y agregar usuarios."""
    if request.method == 'GET':
        users=User.objects.all()
        users_serializer = UserListSerializer(users,many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        user_serializer = UserSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors)
    return None


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_view(request,pk=None):
    """La función user_detail_view permite ver, actualizar y eliminar un usuario específico."""
    #query
    user = User.objects.filter(id = pk).first()
    #validation
    if user:
        if request.method == 'GET':
            user_serializer = UserListSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PUT':
            user_serializer = UserSerializer(user,data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            user.delete()
            return Response({'message': 'Usuario eliminado correctamente'},
                status=status.HTTP_200_OK)
    return Response({'message':'No se ha encontrado el usuario'},
                    status=status.HTTP_400_BAD_REQUEST)
