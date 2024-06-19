from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from apps.cart.models import CartDetail, Cart
from apps.cart.serializer import CartDetailSerializer

class CartDetailViewset(viewsets.ModelViewSet):
    queryset = CartDetail.objects.all()
    serializer_class = CartDetailSerializer

    def retrieve(self, request, pk=None):
        cart = get_object_or_404(Cart.objects.prefetch_related('cartdetail_set'), pk=pk)
        cart_details = cart.cartdetail_set.all()
        serializer = self.get_serializer(cart_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = self.queryset.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_details = serializer.save()
        response_data = [CartDetailSerializer(cd).data for cd in cart_details]
        return Response(response_data, status=status.HTTP_201_CREATED)
