from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from apps.product.views import (ProductListCreateApiView, 
                                ProductRetrieveUpdateDestroyApiView, 
                                CategoryListApiView,
                                CategoryCreateApiView
                                )

urlpatterns = [
    path('category/list', CategoryListApiView.as_view(), name='category_list'),
    path('category/create', CategoryCreateApiView.as_view(), name='category_create'),
    path('list-create', ProductListCreateApiView.as_view(), name='product_list_create'),
    path('retrieve-update-destroy/<int:pk>/', ProductRetrieveUpdateDestroyApiView.as_view(), name='product_retrieve_update_destroy'),
]

# Configuración para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)