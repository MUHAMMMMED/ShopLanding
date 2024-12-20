from rest_framework import serializers
from .models import *
# # from .models import (
# #     Device,
# #     OperatingSystem,
# #     Location,
# #     DeviceType,
# #     OS,
# #     PeakTime,
# #     Region,
# #     City,
# #     Country,
# #     UserVisit,
# # )

# # class DeviceSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Device
# #         fields = ['id', 'name']

# # class OperatingSystemSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = OperatingSystem
# #         fields = ['id', 'name']

# # class LocationSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Location
# #         fields = ['id', 'name']

# # class DeviceTypeSerializer(serializers.ModelSerializer):
# #     device = DeviceSerializer()  # Nested serializer

# #     class Meta:
# #         model = DeviceType
# #         fields = ['id', 'device', 'date', 'total_visits']

# # class OSSerializer(serializers.ModelSerializer):
# #     operating_system = OperatingSystemSerializer()  # Nested serializer

# #     class Meta:
# #         model = OS
# #         fields = ['id', 'operating_system', 'date', 'total_visits']

# # class PeakTimeSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = PeakTime
# #         fields = ['id', 'hour', 'total_visits', 'date']

# # class RegionSerializer(serializers.ModelSerializer):
# #     location = LocationSerializer()  # Nested serializer

# #     class Meta:
# #         model = Region
# #         fields = ['id', 'location', 'date', 'total_visits']

# # class CitySerializer(serializers.ModelSerializer):
# #     location = LocationSerializer()  # Nested serializer
# #     region = RegionSerializer()  # Nested serializer

# #     class Meta:
# #         model = City
# #         fields = ['id', 'location', 'region', 'date', 'total_visits']

# # class CountrySerializer(serializers.ModelSerializer):
# #     location = LocationSerializer()  # Nested serializer
# #     region = RegionSerializer()  # Nested serializer
# #     device_type = DeviceTypeSerializer()  # Nested serializer
# #     operating_system = OSSerializer()  # Nested serializer
# #     peak_time = PeakTimeSerializer()  # Nested serializer

# #     class Meta:
# #         model = Country
# #         fields = ['id', 'location', 'date', 'total_visits', 'region', 'device_type', 'operating_system', 'peak_time']

# # class UserVisitSerializer(serializers.ModelSerializer):
# #     country = CountrySerializer()  # Nested serializer

# #     class Meta:
# #         model = UserVisit
# #         fields = ['id', 'hashed_ip', 'salt', 'user_cookie', 'browser_fingerprint', 'created_at', 'total_visits', 'country']


# from rest_framework import serializers
# from .models import (
#     Device,
#     OperatingSystem,
#     Location,
#     DeviceType,
#     OS,
#     PeakTime,
#     Region,
#     City,
#     Country,
#     UserVisit,
# )

# # سيريالايزر لجهاز
# class DeviceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Device  # النموذج المستخدم
#         fields = ['id', 'name']  # الحقول التي سيتم تضمينها

# # سيريالايزر لنظام التشغيل
# class OperatingSystemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OperatingSystem  # النموذج المستخدم
#         fields = ['id', 'name']  # الحقول التي سيتم تضمينها

# # سيريالايزر للموقع
# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location  # النموذج المستخدم
#         fields = ['id', 'name']  # الحقول التي سيتم تضمينها

# # سيريالايزر لنوع الجهاز
# class DeviceTypeSerializer(serializers.ModelSerializer):
#     device = DeviceSerializer()  # سيريالايزر متداخل

#     class Meta:
#         model = DeviceType  # النموذج المستخدم
#         fields = ['id', 'device', 'date', 'total_visits']  # الحقول التي سيتم تضمينها

# # سيريالايزر لنظام تشغيل الجهاز
# class OSSerializer(serializers.ModelSerializer):
#     operating_system = OperatingSystemSerializer()  # سيريالايزر متداخل

#     class Meta:
#         model = OS  # النموذج المستخدم
#         fields = ['id', 'operating_system', 'date', 'total_visits']  # الحقول التي سيتم تضمينها

# # سيريالايزر لأوقات الذروة
# class PeakTimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PeakTime  # النموذج المستخدم
#         fields = ['id', 'hour', 'total_visits', 'date']  # الحقول التي سيتم تضمينها

# # سيريالايزر للمنطقة
# class RegionSerializer(serializers.ModelSerializer):
#     location = LocationSerializer()  # سيريالايزر متداخل

#     class Meta:
#         model = Region  # النموذج المستخدم
#         fields = ['id', 'location', 'date', 'total_visits']  # الحقول التي سيتم تضمينها

# # سيريالايزر للمدينة
# class CitySerializer(serializers.ModelSerializer):
#     location = LocationSerializer()  # سيريالايزر متداخل
#     region = RegionSerializer()  # سيريالايزر متداخل

#     class Meta:
#         model = City  # النموذج المستخدم
#         fields = ['id', 'location', 'region', 'date', 'total_visits']  # الحقول التي سيتم تضمينها

# # سيريالايزر للبلد
# class CountrySerializer(serializers.ModelSerializer):
#     location = LocationSerializer()  # سيريالايزر متداخل
#     region = RegionSerializer()  # سيريالايزر متداخل
#     device_type = DeviceTypeSerializer()  # سيريالايزر متداخل
#     operating_system = OSSerializer()  # سيريالايزر متداخل
#     peak_time = PeakTimeSerializer()  # سيريالايزر متداخل

#     class Meta:
#         model = Country  # النموذج المستخدم
#         fields = ['id', 'location', 'date', 'total_visits', 'region', 'device_type', 'operating_system', 'peak_time']  # الحقول التي سيتم تضمينها

# # سيريالايزر لزيارة المستخدم
# class UserVisitSerializer(serializers.ModelSerializer):
#     country = CountrySerializer()  # سيريالايزر متداخل

#     class Meta:
#         model = UserVisit  # النموذج المستخدم
#         fields = ['id', 'hashed_ip', 'salt', 'user_cookie', 'browser_fingerprint', 'created_at', 'total_visits', 'country']  # الحقول التي سيتم تضمينها


  

class CampaignSerializer(serializers.ModelSerializer):
    dictionary_campaign = serializers.CharField(write_only=True)  # Accept campaign name
    dictionary_campaign_name = serializers.CharField(source="dictionary_campaign.name", read_only=True)  # Provide the name in responses
    class Meta:
        model = Campaign
        fields = ["id", "dictionary_campaign", "dictionary_campaign_name"]

    def create(self, validated_data):
        # Get or create CampaignDictionary
        campaign_name = validated_data.pop("dictionary_campaign")
        dictionary_campaign, created = CampaignDictionary.objects.get_or_create(name=campaign_name)
        # Create Campaign
        return Campaign.objects.create(dictionary_campaign=dictionary_campaign, **validated_data)
    


class SourceSerializer(serializers.ModelSerializer):
    dictionary_source = serializers.CharField(write_only=True)  # Accept Source name
    dictionary_source_name = serializers.CharField(source="dictionary_source.name", read_only=True)  # Provide the name in responses
    class Meta:
        model = Source
        fields = ["id", "dictionary_source", "dictionary_source_name"]

    def create(self, validated_data):
        # Get or create  Dictionary
        source_name = validated_data.pop("dictionary_source")
        dictionary_source, created = SourceDictionary.objects.get_or_create(name=source_name)
        # Create Source
        return Source.objects.create(dictionary_source=dictionary_source, **validated_data)
    

class MediumSerializer(serializers.ModelSerializer):
 
    dictionary_medium = serializers.CharField(write_only=True)  # Accept medium name
    dictionary_medium_name = serializers.CharField(source="dictionary_medium.name", read_only=True)  # Provide the name in responses
    class Meta:
        model = Medium
        fields = ["id", "dictionary_medium", "dictionary_medium_name"]

    def create(self, validated_data):
        # Get or create  Dictionary
        source_name = validated_data.pop("dictionary_medium")
        dictionary_medium, created = MediumDictionary.objects.get_or_create(name=source_name)
        # Create Medium
        return Medium.objects.create(dictionary_medium=dictionary_medium, **validated_data)
    
 
 