from rest_framework import viewsets  
# from django.http import JsonResponse
from .helpers import register_visit 
from .models import*
from .serializers import*
# from django.utils import timezone
# from datetime import timedelta, datetime

 
class MediumViewSet(viewsets.ModelViewSet):
    queryset = Medium.objects.all()  
    serializer_class = MediumSerializer  

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()  
    serializer_class = CampaignSerializer  


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()  
    serializer_class = SourceSerializer  




# # عرض البيانات لجهاز
# class DeviceViewSet(viewsets.ModelViewSet):
#     queryset = Device.objects.all()  # استعلام للحصول على جميع الأجهزة
#     serializer_class = DeviceSerializer  # تحديد السيريالايزر المستخدم

# # عرض البيانات لنظام التشغيل
# class OperatingSystemViewSet(viewsets.ModelViewSet):
#     queryset = OperatingSystem.objects.all()  # استعلام للحصول على جميع أنظمة التشغيل
#     serializer_class = OperatingSystemSerializer  # تحديد السيريالايزر المستخدم

# # عرض البيانات للموقع
# class LocationViewSet(viewsets.ModelViewSet):
#     queryset = Location.objects.all()  # استعلام للحصول على جميع المواقع
#     serializer_class = LocationSerializer  # تحديد السيريالايزر المستخدم

# # عرض البيانات لنوع الجهاز
# class DeviceTypeViewSet(viewsets.ModelViewSet):
#     queryset = DeviceType.objects.all()  # استعلام للحصول على جميع أنواع الأجهزة
#     serializer_class = DeviceTypeSerializer  # تحديد السيريالايزر المستخدم

# # عرض البيانات لنظام تشغيل الجهاز
# class OSViewSet(viewsets.ModelViewSet):
#     queryset = OS.objects.all()  # استعلام للحصول على جميع أنظمة تشغيل الأجهزة
#     serializer_class = OSSerializer  # تحديد السيريالايزر المستخدم

# # عرض البيانات لأوقات الذروة
# class PeakTimeViewSet(viewsets.ModelViewSet):
#     queryset = PeakTime.objects.all()  # استعلام للحصول على جميع أوقات الذروة
#     serializer_class = PeakTimeSerializer  # تحديد السيريالايزر المستخدم

# # عرض البيانات للمنطقة
# class RegionViewSet(viewsets.ModelViewSet):
#     queryset = Region.objects.all()  # استعلام للحصول على جميع المناطق
#     serializer_class = RegionSerializer  # تحديد السيريالايزر المستخدم

# # عرض البيانات للمدينة
# class CityViewSet(viewsets.ModelViewSet):
#     queryset = City.objects.all()  # استعلام للحصول على جميع المدن
#     serializer_class = CitySerializer  # تحديد السيريالايزر المستخدم

# # عرض البيانات للبلد
# class CountryViewSet(viewsets.ModelViewSet):
#     queryset = Country.objects.all()  # استعلام للحصول على جميع البلدان
#     serializer_class = CountrySerializer  # تحديد السيريالايزر المستخدم

# # # عرض البيانات لزيارة المستخدم
# class UserVisitViewSet(viewsets.ModelViewSet):
#     queryset = UserVisit.objects.all()  # استعلام للحصول على جميع زيارات المستخدمين
#     serializer_class = UserVisitSerializer  # تحديد السيريالايزر المستخدم
    
 
def home(request):
    response = register_visit(request, product_id=None)   
    return response



 