from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/api/', include('apps.product.routers')),
    path('user/api/', include('apps.user.urls')),

]
