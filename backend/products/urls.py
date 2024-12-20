from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'categories_dash', CategoryView, basename='categories_dash')
router.register(r'products-dash', ProductDashView, basename='products-dash')
router.register(r'image', ImageViewSet, basename='image')

 
urlpatterns = [
 
    path('create/', ProductSet.as_view(), name='product-create'),
    # URL to update a specific Product by ID
    path('update/<int:pk>/', ProductSet.as_view(), name='product-update'),
    # URL to delete a specific Product by ID
    path('delete/<int:pk>/', ProductSet.as_view(), name='product-delete'),
    
    path('product_list_dash/', ProductListAPIView.as_view(), name='product-list-dash'),
   
]

# Include the router URLs
urlpatterns += router.urls







 