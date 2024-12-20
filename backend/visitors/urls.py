from django.urls import path, include  # استيراد المسارات وinclude من Django
from rest_framework.routers import DefaultRouter  # استيراد DefaultRouter من Django Rest Framework
from .views import *  # استيراد جميع الـ Views من الملف الحالي
from visitors.views import *  # استيراد RecordVisitorView من ملف visitors.views

# # إنشاء راوتر لتسهيل التعامل مع URLs
router = DefaultRouter()
# router.register(r'devices', DeviceViewSet)  # تسجيل DeviceViewSet مع المسار /devices/
# router.register(r'operating-systems', OperatingSystemViewSet)  # تسجيل OperatingSystemViewSet مع المسار /operating-systems/
# router.register(r'locations', LocationViewSet)  # تسجيل LocationViewSet مع المسار /locations/
# router.register(r'device-types', DeviceTypeViewSet)  # تسجيل DeviceTypeViewSet مع المسار /device-types/
# router.register(r'os', OSViewSet)  # تسجيل OSViewSet مع المسار /os/
# router.register(r'peak-times', PeakTimeViewSet)  # تسجيل PeakTimeViewSet مع المسار /peak-times/
# router.register(r'regions', RegionViewSet)  # تسجيل RegionViewSet مع المسار /regions/
# router.register(r'cities', CityViewSet)  # تسجيل CityViewSet مع المسار /cities/
# router.register(r'countries', CountryViewSet)  # تسجيل CountryViewSet مع المسار /countries/
# router.register(r'user-visits', UserVisitViewSet)  # تسجيل UserVisitViewSet مع المسار /user-visits/

router.register(r'medium', MediumViewSet)  
router.register(r'campaign', CampaignViewSet)  
router.register(r'source', SourceViewSet) 

 

# تعريف الـ urlpatterns
urlpatterns = [
    # path('record-visitor/', RecordVisitorView.as_view(), name='record-visitor'),  # إضافة مسار لتسجيل الزيارة
    path('home/', home, name='home'),  # إضافة مسار للصفحة الرئيسية
    # path('', include(router.urls)),  # تضمين جميع URLs من الراوتر
]
# Include the router URLs
urlpatterns += router.urls
 

 