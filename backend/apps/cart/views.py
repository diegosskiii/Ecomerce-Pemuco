from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.cart.models import Cart_detail
from apps.cart.serializer import CartDetailSerializer

class CartDetailViewset(viewsets.ModelViewSet):
    queryset = Cart_detail.objects.all()
    serializer_class = CartDetailSerializer

    def retrieve(self, request, pk=None):
        try:
            cart_detail = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(cart_detail)
            return Response(serializer.data)
        except Cart_detail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
