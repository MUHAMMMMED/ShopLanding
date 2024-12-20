سأوفر هنا أساسًا بسيطًا لبناء هيكل الموقعين باستخدام Django لتقديم خدمات الإيجار وخدمات المجتمع للمستأجرين. سأركز على إنشاء النماذج الأساسية، إعداد API باستخدام Django REST Framework، وإنشاء بعض النهايات الأساسية (API Endpoints) لبدء العمل على الموقعين.

١. إعداد مشروع Django

قم أولاً بإنشاء مشروع Django جديد مع تطبيقين: واحد للإيجار (rentals) وواحد للمجتمع (community).

إنشاء مشروع Django

django-admin startproject housing_project
cd housing_project
python manage.py startapp rentals
python manage.py startapp community

٢. إنشاء النماذج (Models) الأساسية

في هذه الخطوة، سننشئ النماذج الأساسية لكل من تطبيقي الإيجار والمجتمع.

نموذج Property لتطبيق الإيجار (rentals/models.py)

from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return self.title

نموذج RentalContract لتطبيق الإيجار (rentals/models.py)

class RentalContract(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='contracts')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    terms = models.TextField()

    def __str__(self):
        return f"Contract for {self.property.title} by {self.tenant.username}"

نموذج CommunityMember لتطبيق المجتمع (community/models.py)

class CommunityMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Community Member: {self.user.username}"

نموذج MaintenanceRequest لتطبيق المجتمع (community/models.py)

class MaintenanceRequest(models.Model):
    member = models.ForeignKey(CommunityMember, on_delete=models.CASCADE, related_name='maintenance_requests')
    issue = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    request_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Request: {self.issue} by {self.member.user.username}"

٣. إنشاء واجهة برمجة التطبيقات (APIs) باستخدام Django REST Framework

قم بتثبيت Django REST Framework:

pip install djangorestframework

ثم قم بإضافتها إلى INSTALLED_APPS في settings.py.

إعداد Serializer لتطبيق الإيجار (rentals/serializers.py)

from rest_framework import serializers
from .models import Property, RentalContract

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class RentalContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalContract
        fields = '__all__'

إعداد Serializer لتطبيق المجتمع (community/serializers.py)

from rest_framework import serializers
from .models import CommunityMember, MaintenanceRequest

class CommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = '__all__'

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = '__all__'

٤. إنشاء API Views للتفاعل مع الواجهة الأمامية

عرض العقارات في تطبيق الإيجار (rentals/views.py)

from rest_framework import viewsets
from .models import Property, RentalContract
from .serializers import PropertySerializer, RentalContractSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class RentalContractViewSet(viewsets.ModelViewSet):
    queryset = RentalContract.objects.all()
    serializer_class = RentalContractSerializer

إدارة طلبات الصيانة في تطبيق المجتمع (community/views.py)

from rest_framework import viewsets
from .models import CommunityMember, MaintenanceRequest
from .serializers import CommunityMemberSerializer, MaintenanceRequestSerializer

class CommunityMemberViewSet(viewsets.ModelViewSet):
    queryset = CommunityMember.objects.all()
    serializer_class = CommunityMemberSerializer

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer

٥. إعداد URL Routing

في housing_project/urls.py، أضف الروابط للـ API.

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rentals import views as rental_views
from community import views as community_views

router = DefaultRouter()
router.register(r'properties', rental_views.PropertyViewSet)
router.register(r'rental_contracts', rental_views.RentalContractViewSet)
router.register(r'community_members', community_views.CommunityMemberViewSet)
router.register(r'maintenance_requests', community_views.MaintenanceRequestViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

٦. تشغيل المشروع واختباره

يمكنك الآن تشغيل المشروع والتحقق من أن الـ API جاهزة وتعمل بشكل جيد:

python manage.py migrate
python manage.py runserver

ملاحظات إضافية

	•	التصميم: يمكنك استخدام React لبناء واجهة أمامية تعرض البيانات من API باستخدام مكونات مناسبة لكل صفحة (صفحة العقارات، لوحة التحكم للمستأجرين، إلخ).
	•	التسجيل الموحد: يمكنك استخدام OAuth أو مكتبة مثل django-allauth لتوفير تسجيل دخول موحد بين الموقعين.
	•	التكامل المستقبلي: يمكنك توسيع المشروع بإضافة مزايا مثل التنبيهات، الإشعارات، وربط الحسابات الاجتماعية.

هذا الإعداد سيمنحك هيكلاً أولياً لبناء الموقعين مع إمكانيات التوسع مستقبلاً.