"""
Este módulo define las URL (Uniform Resource Locator) de la aplicación de usuarios.

Módulos externos requeridos:
- django.urls: Proporciona herramientas para definir las URL de una aplicación Django.

URLs:
- '/users/': URL para las operaciones de lista y creación de usuarios.
- '/': URL para la autenticación de usuarios.
- '/detail/<int:pk>/': URL para las operaciones de detalle,
    actualización y eliminación de un usuario específico.

Funciones y Clases de Vistas:
    - user_api_view: Vista para mostrar y agregar usuarios.
    - user_detail_view: Vista para ver, actualizar y eliminar un usuario específico.
    - Login: Vista para la autenticación de usuarios.

"""
from django.urls import path
from apps.user.views import user_api_view, user_detail_view, Login, Logout

urlpatterns = [
    path('users/', user_api_view, name='user_api'),
    path('', Login.as_view(),name='Login'),
    path('logout/', Logout.as_view(),name='Logout'),
    path('detail/<int:pk>/', user_detail_view, name='user_detail_api')
]