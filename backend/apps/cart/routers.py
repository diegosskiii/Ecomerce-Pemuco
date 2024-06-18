from rest_framework.routers import DefaultRouter
from apps.cart.views import CartDetailViewset

router = DefaultRouter()

router.register(r'cart',CartDetailViewset, basename='cart')

urlpatterns = router.urls