from rest_framework import serializers
from .models import *
from cart.models import Coupon
from datetime import datetime
from content.models import Settings

class Image_ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Product
        fields = '__all__'

 
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    images = Image_ProductSerializer(many=True)
    currency = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()
    today = datetime.today().date()

    class Meta:
        model = Product
        fields = '__all__'

    def get_category_name(self, obj):
        """Retrieve category name safely."""
        return obj.category.name if obj.category else None

    def get_currency(self, obj):
       """Retrieve currency settings with a fallback for missing data."""
       settings = Settings.objects.first()  # Fetch the first settings record
       if settings:
        # Return one currency value as a string based on language preference
         if obj.language == 'ar':
            return settings.currency_ar
         else:
            return settings.currency_en
       return 'Currency not available'

    def get_coupon(self, obj):
        """Retrieve the first valid coupon, ordered by expiry date."""
        coupon = Coupon.objects.filter(
            expiryDate__gte=self.today,
            coupon_usage__gt=0
        ).order_by('-expiryDate').only('code', 'discount', 'expiryDate').first()

        if coupon:
            return {
                "code": coupon.code,
                "discount": coupon.discount,
                "expiryDate": coupon.expiryDate,
            }
        return None







 
class Image_ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Product
        fields = '__all__'

    def create(self, validated_data):
        product_id = self.context.get('product_id')
        if not product_id:
            raise serializers.ValidationError({"product_id": "Product ID is required."})
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Invalid Product ID."})
        image_product = Image_Product.objects.create(**validated_data)
        product.images.add(image_product)
        return image_product




# class Product_Serializer(serializers.ModelSerializer):
#     images = serializers.ListField(
#         child=serializers.ImageField(), write_only=True, required=False  )
#     images_urls = serializers.SerializerMethodField(read_only=True)   
#     class Meta:
#         model = Product
#         fields = '__all__'

#     def create(self, validated_data):
#         images_data = validated_data.pop('images', [])
#         product = Product.objects.create(**validated_data)

#         image_products = [
#             Image_Product(image=image) for image in images_data
#         ]
#         # Bulk create Image_Product instances
#         Image_Product.objects.bulk_create(image_products)
        
#         # Add them to the product's images field
#         product.images.add(*image_products)

#         return product
 
#     def get_images_urls(self, obj):
#         # Retrieve image URLs
#         return [image.image.url for image in obj.images.all()]

class Product_Serializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False)
    images_urls = serializers.SerializerMethodField(read_only=True) 

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)

        image_products = [
            Image_Product(image=image) for image in images_data
        ]
        # Bulk create Image_Product instances
        Image_Product.objects.bulk_create(image_products)

        # Add them to the product's images field
        product.images.add(*image_products)

        return product


    def get_images_urls(self, obj):
        # Retrieve image URLs
        return [image.image.url for image in obj.images.all()]



class Product_update_Serializer(serializers.ModelSerializer):
  
    class Meta:
        model = Product
        fields = '__all__'
    def update(self, instance, validated_data):
 
        validated_data.pop('images', None)
        return super().update(instance, validated_data)

  






class CategorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)  # استخدم related_name 'products'
    class Meta:
        model = Category
        fields = '__all__'

