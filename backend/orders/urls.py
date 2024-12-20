from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
 
router.register(r'orders-list', OrdersViewSet, basename='orders-list')
router.register(r'shipping-countries_dash',shipping_CountryDash, basename='shipping-countries_dash')
router.register(r'shipping-companies_dash', Shipping_CompanyDash, basename='shipping-companies_dash')

router.register(r'shipping-companies', Shipping_CompanyViewSet, basename='shipping-companies')
router.register(r'shipping-countries', shipping_CountryViewSet, basename='shipping-countries')
router.register(r'customer', CustomerViewSet, basename='customer')

 

urlpatterns = [
  
    path('shipping-company/<int:id>/', Shipping_CompanyAPIView.as_view(), name='shipping-Company'),
    path('shipping/<int:id>/', ShippingAPIView.as_view(), name='shipping'),
    path('order/',OrderAPIView.as_view()),
    path('order-detail/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
    path('<int:pk>/delete/', DeleteOrder.as_view(), name='delete_order'),
    path('status/<int:pk>/',  UpdateStatus.as_view(), name='update-order-status'),
    path('anticipation/<int:pk>/', UpdateAnticipation.as_view(), name='update-order-anticipation'),
    path('package/<int:pk>/',  UpdatePackage.as_view(), name='update-order-package_type'),
    path('invoice/',InvoiceDetail.as_view(), name='invoice'),
 
 
]

# Include the router URLs
urlpatterns += router.urls







 