from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
urlpatterns = [
 
    path('api/content/', include('content.urls')),
    path('api/visitors/', include('visitors.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/Users/', include('accounts.urls')),
    path('api/payment/', include('payment.urls')),
    path('api/admin/', admin.site.urls),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 

 
    
