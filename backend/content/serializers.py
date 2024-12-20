from rest_framework import serializers
from .models import *
from products.serializers import * 
from visitors.serializers import CampaignSerializer,SourceSerializer,MediumSerializer

 
class HeaderModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderModule
        fields = '__all__'

class SliderModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderModule
        fields = '__all__'

class ContentModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentModule
        fields = '__all__'

class FooterModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterModule
        fields = '__all__'


 
class ModuleSerializer(serializers.ModelSerializer):
    header = HeaderModuleSerializer(required=False)
    slider = SliderModuleSerializer(required=False)
    content = ContentModuleSerializer(required=False)
    footer = FooterModuleSerializer(required=False)
    product = ProductSerializer(required=False)
 
    class Meta:
        model = Module
        fields = ['id','unique_id', 'module_type', 'mobile_order','tablet_order','desktop_order', 'header', 'slider','product', 'content', 'footer']  # Make sure 'unique_id' is in this list
        
 

class SectionSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, required=False)  # التأكد من أن الموديولات ليست مطلوبة
    class Meta:
        model = Section
        fields = '__all__'

    def create(self, validated_data):
        modules_data = validated_data.pop('modules', None)  # إزالة البيانات الخاصة بالموديولات
        section = Section.objects.create(**validated_data)
        if modules_data:
            for module_data in modules_data:
                Module.objects.create(section=section, page=module_data['page'].id, **module_data)
        return section

    def update(self, instance, validated_data):
        modules_data = validated_data.pop('modules', None)
        instance.title = validated_data.get('title', instance.title)
        # instance.order = validated_data.get('order', instance.order)
        instance.mobile_order = validated_data.get('mobile_order', instance.mobile_order)
        instance.tablet_order = validated_data.get('tablet_order', instance.tablet_order)
        instance.desktop_order = validated_data.get('desktop_order', instance.desktop_order)
        instance.save()  
        
        if modules_data:
           
            print("Modules data provided for update:", modules_data)  # تتبع الموديولات

        return instance

  
class LinksSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer( read_only=True)
    source = SourceSerializer( read_only=True)
    medium = MediumSerializer(read_only=True)

    class Meta:
        model = Links
        fields = '__all__'

 




class PageSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, required=False)   
    class Meta:
        model = Page
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop('sections', None)   
        page = Page.objects.create(**validated_data)  
        return page

    def update(self, instance, validated_data):
        validated_data.pop('sections', None)  
        instance.title = validated_data.get('title', instance.title)  # تحديث العنوان إذا تم توفيره
        instance.save()  
        return instance 
    


# class LinksSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Links
#         fields = '__all__'




 
# class HomeSerializer(serializers.ModelSerializer):
#     page = PageSerializer()  

#     class Meta:
#         model = Home
#         fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'
 

class Settings_Serializer(serializers.ModelSerializer):
    home = PageSerializer( read_only=True)
    # (required=False)
    # about = PageSerializer(required=False)
    # privacy = PageSerializer(required=False)
    # contactUs = PageSerializer(required=False)
  
    class Meta:
        model = Settings
        fields = '__all__'

   