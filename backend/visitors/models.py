from django.db import models
from django.utils import timezone

class Date(models.Model):
    date = models.DateField(default=timezone.now, unique=True)

    def __str__(self):
        return str(self.date)

class Hour(models.Model):
    hour = models.IntegerField(unique=True)
    def __str__(self):
        return f"{self.hour}:00"

# class Declaration(models.Model):
#     duration = models.IntegerField(unique=True)

#     def __str__(self):
#         return f"{self.duration} minutes"

 
class Device(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
 
    
class BrowserDictionary(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Browser(models.Model):
    # name = models.ForeignKey(BrowserDictionary, on_delete=models.CASCADE, related_name='Browser')
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class OperatingSystem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class PlaceDictionary(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Region(models.Model):
    place_name = models.ForeignKey(PlaceDictionary, on_delete=models.CASCADE, related_name='regions')
 
    def __str__(self):
        return f"Region: {self.place_name.name}"
 

class Country(models.Model):
    place_name = models.ForeignKey(PlaceDictionary, on_delete=models.CASCADE, related_name='countries')

    def __str__(self):
        return f"Country: {self.place_name.name}"
 
class State(models.Model):
    place_name = models.ForeignKey(PlaceDictionary, on_delete=models.CASCADE, related_name='state')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='state')

    class Meta:
        unique_together = ('place_name', 'country')

    def __str__(self):
        return f"state: {self.place_name.name} in {self.country}"


class City(models.Model):
    place_name = models.ForeignKey(PlaceDictionary, on_delete=models.CASCADE, related_name='cities')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        unique_together = ('place_name', 'state')

    def __str__(self):
        return f"City: {self.place_name.name} in {self.state}"

class UserVisit(models.Model):
    created_at= models.ForeignKey(Date, on_delete=models.CASCADE)
    hashed_ip = models.CharField(max_length=64, unique=True)
    salt = models.CharField(max_length=16)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='user_visits', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='user_visits', blank=True, null=True)
    user_cookie = models.CharField(max_length=255, blank=True, null=True)
    browser_fingerprint = models.CharField(max_length=255, blank=True, null=True)
    total_visits = models.IntegerField(default=1)
    device_type = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='user_visits', blank=True, null=True)
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.CASCADE, related_name='user_visits', blank=True, null=True)
    browser = models.ForeignKey(Browser, on_delete=models.CASCADE, related_name='user_visits', blank=True, null=True)
   

    
    def __str__(self):
        return f"Visit on {self.created_at} from {self.country}"
 



class SourceDictionary(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class MediumDictionary(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CampaignDictionary(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
 
 

class Source(models.Model):
    dictionary_source = models.ForeignKey(SourceDictionary, on_delete=models.CASCADE, related_name='sources')

    def __str__(self):
        return f"Source: {self.dictionary_source.name}"


class Medium(models.Model):
    dictionary_medium = models.ForeignKey(MediumDictionary, on_delete=models.CASCADE, related_name='media')

    def __str__(self):
        return f"Medium: {self.dictionary_medium.name}"  # Corrected to access the right field


class Campaign(models.Model):
    dictionary_campaign = models.ForeignKey(CampaignDictionary, on_delete=models.CASCADE, related_name='campaigns')

    def __str__(self):
        return f"Campaign: {self.dictionary_campaign.name}"  # Corrected to access the right field


class HourlyVisit(models.Model):
    user_visit = models.ForeignKey(UserVisit, on_delete=models.CASCADE, related_name='hourly_visits')
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE, related_name='hourly_visits')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='hourly_visits')
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='hourly_visits')
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE, related_name='hourly_visits')

    def __str__(self):
        return f"Hourly Visit by User: {self.user_visit.id} on {self.date} at {self.hour}"


class ProductHourlyVisit(models.Model):
    user_visit = models.ForeignKey(UserVisit, on_delete=models.CASCADE, related_name='product_hourly_visits')
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE, related_name='product_hourly_visits')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='product_hourly_visits')
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='product_hourly_visits')
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE, related_name='product_hourly_visits')

    def __str__(self):
        return f"Product Hourly Visit by User: {self.user_visit.id} on {self.date} at {self.hour}"








# لجلب كل المدن في دولة معينة
# country = Country.objects.get(place_name__name="Egypt")
# regions = country.regions.all()
# for region in regions:
#     cities = region.cities.all()


# from django.db.models import Q

# # نفترض أن أسماء الدولة والمنطقة والمدينة موجودة بالفعل في PlaceDictionary
# country_name = "مصر"
# region_name = "القاهرة الكبرى"
# city_name = "القاهرة"


# # نبدأ بتنفيذ الاستعلام
# user_visits = UserVisit.objects.filter(
#     country__name__name=country_name,
#     region__name__name=region_name,
#     city__name__name=city_name
# )


# تحسين الاستعلام باستخدام Q للمرونة

# إذا كنت تحتاج إلى استعلام أكثر مرونة، وتريد البحث عن زيارات تتطابق مع دولة أو منطقة أو مدينة معينة فقط، يمكنك استخدام كائنات Q لدمج شروط متعددة في استعلام واحد:


# from django.db.models import Q

# user_visits = UserVisit.objects.filter(
#     Q(country__name__name=country_name) &
#     Q(region__name__name=region_name) &
#     Q(city__name__name=city_name)
# )


# for visit in user_visits:
#     print(f"User Visit ID: {visit.id}, Country: {visit.country.name}, Region: {visit.region.name}, City: {visit.city.name}")


# from django.db.models import Q
# from django.utils import timezone

# # افتراض التواريخ المطلوبة لنطاق البحث
# start_date = timezone.datetime(2024, 1, 1)
# end_date = timezone.datetime(2024, 12, 31)

# # بيانات المواقع التي نبحث عنها
# country_name = "مصر"
# region_name = "القاهرة الكبرى"
# city_name = "القاهرة"

# # استعلام لتصفية البيانات بناءً على نطاق التاريخ والموقع
# user_visits = UserVisit.objects.filter(
#     Q(date__date__range=(start_date, end_date)) &  # فلترة ضمن نطاق التاريخ
#     Q(country__name__name=country_name) &          # فلترة على أساس الدولة
#     Q(region__name__name=region_name) &            # فلترة على أساس المنطقة
#     Q(city__name__name=city_name)                  # فلترة على أساس المدينة
# )


# device_name = "هاتف محمول"
# os_name = "Android"
# source_name = "Google"
# medium_name = "Organic"

# user_visits = UserVisit.objects.filter(
#     Q(date__date__range=(start_date, end_date)) &
#     Q(country__name__name=country_name) &
#     Q(region__name__name=region_name) &
#     Q(city__name__name=city_name) &
#     Q(device__name__name=device_name) &
#     Q(operating_system__name__name=os_name) &
#     Q(source__dictionary_source__name=source_name) &
#     Q(medium__dictionary_medium__name=medium_name)
# )


# user_visits = UserVisit.objects.filter(
#     date__date__range=(start_date, end_date)
# )

# # للوصول إلى hourly visits لكل user_visit
# for visit in user_visits:
#     hourly_visits = visit.hourly_visits.all()  # هذا سيجلب جميع الساعات المرتبطة بهذه الزيارة





 