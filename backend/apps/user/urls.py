from django.urls import path, include
from apps.user.views import user_api_view, user_detail_view, Login

urlpatterns = [
    path('users/', user_api_view, name='user_api'),
    path('', Login.as_view(),name='Login'),
    path('detail/<int:pk>/', user_detail_view, name='user_detail_api')
]