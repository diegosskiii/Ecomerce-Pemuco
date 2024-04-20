from rest_framework.routers import DefaultRouter
from apps.product.views import ProductViewSet, CategoryViewSet

router = DefaultRouter()

router.register(r'product',ProductViewSet, basename='product')
router.register(r'category',CategoryViewSet, basename='category')

urlpatterns = router.urls