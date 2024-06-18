from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.product.serializer import ProductSerializer, CategorySerializer

#category viewsets
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Created category'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    

        
#porduct viewsets
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        else:
            return self.get_serializer().Meta.model.objects.filter(state=True, product_id=pk).first()
        
    def list(self,request):
        product_serializer = self.get_serializer(self.get_queryset(),many=True)
        return Response(product_serializer.data, status= status.HTTP_200_OK)

    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Producto creado'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk),data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response(product_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        product = self.get_queryset().filter(product_id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Removed product'}, status=status.HTTP_200_OK)
        return Response({'message':'The product does not exist'}, status= status.HTTP_400_BAD_REQUEST)
