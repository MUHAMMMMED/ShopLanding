from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

 
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
 
class CategoryView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
  
class ProductDashView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

 

class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        # Retrieve query parameters
        category = request.query_params.get('category', None)
        ssku = request.query_params.get('ssku', None)
        name = request.query_params.get('name', None)
        # Build query dynamically
        filters = Q()
        if category:
            filters &= Q(category_id=category)
        if ssku:
            filters &= Q(ssku__icontains=ssku)
        if name:
            filters &= Q(name__icontains=name)

        # Query the database
        products = Product.objects.filter(filters)

        # Serialize and return response
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data}, status=status.HTTP_200_OK)
  


 
class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Image_Product.objects.all()
    serializer_class = Image_ProductSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        product_id = self.request.data.get('product_id')
        if product_id:
            context['product_id'] = product_id
        return context


class ProductSet(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        serializer = Product_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        # print(request.data)
        serializer = Product_update_Serializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        # Check if pk is provided
        if pk is None:
            return Response({"error": "Product ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

  