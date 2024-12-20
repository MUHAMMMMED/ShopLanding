from rest_framework import serializers
from .models import *
from products.serializers import *
 

 
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





 

# class Product_Serializer(serializers.ModelSerializer):
#     # tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
#     images = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

#     class Meta:
#         model = Product
#         fields = '__all__'

#     def create(self, validated_data):
 
#         images_data = validated_data.pop('images', [])

#         # إنشاء المنتج
#         product = Product.objects.create(**validated_data)

#         # التعامل مع الصور: ربط الصور بالمنتج
#         for image_url in images_data:
#             image_product = Image_Product.objects.create(image=image_url)
#             product.images.add(image_product)

#         return product

# class Product_Serializer(serializers.ModelSerializer):
#     images = serializers.ListField(
#         child=serializers.CharField(), write_only=True, required=False
#     )

#     class Meta:
#         model = Product
#         fields = '__all__'

#     def create(self, validated_data):
#         # استخراج الصور من البيانات المرسلة
#         images_data = validated_data.pop('images', [])

#         # إنشاء المنتج
#         product = Product.objects.create(**validated_data)

#         # التعامل مع الصور: التحقق من صحة الروابط وحفظها
#         for image_url in images_data:
#             if self._is_valid_url(image_url):
#                 # إنشاء صورة وربطها بالمنتج
#                 image_product = Image_Product.objects.create(image=image_url)
#                 product.images.add(image_product)
#             else:
#                 raise serializers.ValidationError(f"Invalid image URL: {image_url}")

#         return product

#     def _is_valid_url(self, url):
#         """Helper method to validate URLs."""
#         import re
#         # تحقق من وجود بروتوكول وصيغة رابط صالح
#         url_regex = re.compile(
#             r'^(http|https)://[^\s/$.?#].[^\s]*\.(jpg|jpeg|png|gif|webp)$', re.IGNORECASE
#         )
#         return re.match(url_regex, url) is not None




# class Product_Serializer(serializers.ModelSerializer):
#     images = serializers.ListField(
#         child=serializers.ImageField(), write_only=True, required=False
#     )

#     class Meta:
#         model = Product
#         fields = '__all__'

#     def create(self, validated_data):
#         images_data = validated_data.pop('images', [])
#         product = Product.objects.create(**validated_data)

#         for image in images_data:
#             # Save the image to the database or attach it to the product
#             image_product = Image_Product.objects.create(image=image)
#             product.images.add(image_product)

#         return product


# class Product_Serializer(serializers.ModelSerializer):
#     images = serializers.ListField(
#         child=serializers.ImageField(), write_only=True, required=False
#     )

#     class Meta:
#         model = Product
#         fields = '__all__'

#     def create(self, validated_data):
#         images_data = validated_data.pop('images', [])
#         product = Product.objects.create(**validated_data)

#         for image in images_data:
#             image_product = Image_Product.objects.create(image=image)
#             product.images.add(image_product)

#         return product







# class Product_Serializer(serializers.ModelSerializer):
#     tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
#     images = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

#     class Meta:
#         model = Product
#         fields = '__all__'

#     def create(self, validated_data):
#         # إزالة التاجز والإيميج من البيانات
#         tags_data = validated_data.pop('tags', [])
#         images_data = validated_data.pop('images', [])

#         # إنشاء المنتج
#         product = Product.objects.create(**validated_data)

#         # التعامل مع التاجز: ربط التاجز بالمنتج
#         tags = [Tags.objects.get_or_create(name=tag_name)[0] for tag_name in tags_data]
#         product.tags.set(tags)  # إضافة التاجز دفعة واحدة

#         # التعامل مع الصور: ربط الصور بالمنتج
#         images = [Image_Product(image=image_url) for image_url in images_data]
#         Image_Product.objects.bulk_create(images)  # إضافة الصور دفعة واحدة
#         product.images.add(*images)  # ربط الصور بالمنتج

#         return product

#     def update(self, instance, validated_data):
#         # إزالة التاجز والإيميج من البيانات
#         tags_data = validated_data.pop('tags', [])
#         images_data = validated_data.pop('images', [])

#         # تحديث المنتج
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         # التعامل مع التاجز: ربط التاجز بالمنتج
#         tags = [Tags.objects.get_or_create(name=tag_name)[0] for tag_name in tags_data]
#         instance.tags.set(tags)  # إضافة التاجز دفعة واحدة

#         # التعامل مع الصور: تحديث الصور
#         existing_images = set(instance.images.all())
#         new_images = {Image_Product(image=image_url) for image_url in images_data}
        
#         # حذف الصور القديمة التي لم تعد موجودة
#         for image in existing_images - new_images:
#             image.delete()

#         # إضافة الصور الجديدة دفعة واحدة
#         images = [Image_Product(image=image_url) for image_url in images_data if image_url not in existing_images]
#         Image_Product.objects.bulk_create(images)
#         instance.images.add(*images)  # ربط الصور بالمنتج

#         return instance
















 

# class PageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Page
#         fields = '__all__'

    # def validate_keywords(self, value):
    #     # Add validation for keywords if needed
    #     if not isinstance(value, str):
    #         raise serializers.ValidationError("Keywords must be a string.")
    #     return value

class ModuleSerializer(serializers.ModelSerializer):
    header = HeaderModuleSerializer(required=False)
    slider = SliderModuleSerializer(required=False)
    content = ContentModuleSerializer(required=False)
    footer = FooterModuleSerializer(required=False)
    product = ProductSerializer(required=False)
 
    class Meta:
        model = Module
        fields = ['id','unique_id', 'module_type', 'mobile_order','tablet_order','desktop_order', 'header', 'slider','product', 'content', 'footer']  # Make sure 'unique_id' is in this list
        


# class SectionSerializer(serializers.ModelSerializer):
#     modules = ModuleSerializer(many=True)

#     class Meta:
#         model = Section
#         fields = '__all__'

 
 
# class SectionSerializer(serializers.ModelSerializer):
#     modules = ModuleSerializer(many=True, required=False)  # التأكد من أن الموديولات ليست مطلوبة

#     class Meta:
#         model = Section
#         fields = '__all__'

#     def create(self, validated_data):
#         modules_data = validated_data.pop('modules', None)  # إزالة البيانات الخاصة بالموديولات
#         # إنشاء قسم جديد
#         section = Section.objects.create(**validated_data)

#         # إذا كان هناك موديولات، يجب عليك إنشائها وربطها بالقسم
#         if modules_data:
#             for module_data in modules_data:
#                 Module.objects.create(section=section,page=module_data.page.id, **module_data)  # تأكد من أن لديك العلاقة الصحيحة
                                        
#         return section  # إرجاع الكائن الذي تم إنشاؤه

#         def update(self, instance, validated_data):
#           modules_data = validated_data.pop('modules', None)
#           instance.title = validated_data.get('title', instance.title)
#           instance.order = validated_data.get('order', instance.order)
#           instance.mobile_order = validated_data.get('mobile_order', instance.mobile_order)
#           instance.tablet_order = validated_data.get('tablet_order', instance.tablet_order)
#           instance.desktop_order = validated_data.get('desktop_order', instance.desktop_order)
#           instance.save()  # حفظ الكائن بعد التحديث
#           return instance  # إرجاع الكائن المحدث
 
    #     def update(self, instance, validated_data):

    
    #       # Check if instance is saved correctly
    #       try:
    #        instance.save()
    #       except serializers.ValidationError as e:
    #        print(f"Validation Error: {e}")  # Log validation errors
    #        raise

    # # Handle modules data if needed
    #       return instance
 
 

# class SectionSerializer(serializers.ModelSerializer):
#     modules = ModuleSerializer(many=True, required=False)  # Ensure modules are not required

#     class Meta:
#         model = Section
#         fields = '__all__'

#     def create(self, validated_data):
#         modules_data = validated_data.pop('modules', None)  # Remove modules data
#         section = Section.objects.create(**validated_data)

#         if modules_data:
#             for module_data in modules_data:
#                 Module.objects.create(section=section, page=module_data.get('page', None), **module_data)
                                        
#         return section  # Return the created object

#     def update(self, instance, validated_data):
#         modules_data = validated_data.pop('modules', None)
#         instance.title = validated_data.get('title', instance.title)
#         instance.page = validated_data.get('page', instance.page)
#         instance.order = validated_data.get('order', instance.order)
#         instance.mobile_order = validated_data.get('mobile_order', instance.mobile_order)
#         instance.tablet_order = validated_data.get('tablet_order', instance.tablet_order)
#         instance.desktop_order = validated_data.get('desktop_order', instance.desktop_order)

#         try:
#             instance.save()  # Save the updated instance
#         except Exception as e:
#             print(f"Error while updating Section: {e}")  # Log the error
#             raise serializers.ValidationError("Error updating section.")

        # return instance  # Return the updated object




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
        print("Updating Section with data:", validated_data)  
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

 


class PageSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, required=False)  # اجعل الحقل غير مطلوب
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
        instance.save()  # حفظ الكائن بعد التحديث
        return instance  # إرجاع الكائن المحدث
    



# class ProductSerializer(serializers.ModelSerializer):
 
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'date','category_name']

# class CategorySerializer(serializers.ModelSerializer):
#     product = ProductSerializer(many=True, read_only=True)

#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'product']
    


# serializers.py
 





class HomeSerializer(serializers.ModelSerializer):
    page = PageSerializer()  # Add the PageSerializer here to include related Page data

    class Meta:
        model = Home
        fields = '__all__'