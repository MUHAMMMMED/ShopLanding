from rest_framework import serializers
from .models import *
from cart.serializers import NoteSerializer

class Order_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
 

class DictionaryProductNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictionaryProductName
        fields = '__all__'
 

 
class OrderItemSerializer(serializers.ModelSerializer):
    dictionary = DictionaryProductNameSerializer()
    # order = Order_Serializer()  
    notes = NoteSerializer(many=True)   

    class Meta:
        model = OrderItem
        fields = '__all__'





class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()   
    order_items = OrderItemSerializer(many=True, read_only=True)  
    class Meta:
        model = Order
        fields = '__all__'

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None  # Note the change here

 
class Shipping_CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping_Company
        fields = '__all__'

    def create(self, validated_data):
        # Retrieve Country ID from the context
        Country_id = self.context.get('Country_id')
        if not Country_id:
            raise serializers.ValidationError({"Country_id": "Country ID is required."})
        
        try:
            # Fetch the shipping_Country instance
            country = shipping_Country.objects.get(id=Country_id)
        except shipping_Country.DoesNotExist:
            raise serializers.ValidationError({"Country_id": "Invalid Country ID."})

        # Create the Shipping_Company instance
        shipping_company = Shipping_Company.objects.create(**validated_data)
        country.Shipping.add(shipping_company)  # Associate the shipping company with the country
        return shipping_company
 











  
class shipping_CountrySerializer(serializers.ModelSerializer):
    Shipping = Shipping_CompanySerializer(many=True, read_only=True)  # Make it read-only

    class Meta:
        model = shipping_Country
        fields = "__all__"

    def create(self, validated_data):
        # Remove 'Shipping' from validated_data if it exists
        validated_data.pop('Shipping', None)
        
        # Create the shipping_Country instance
        return shipping_Country.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Remove 'Shipping' from validated_data if it exists
        validated_data.pop('Shipping', None)
        
        # Update the instance with remaining data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

 



class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

 
# class shipping_CountrySerializer(serializers.ModelSerializer):
#     Shipping = serializers.StringRelatedField(many=True)  

#     class Meta:
#         model = shipping_Country
#         fields = "__all__"

 




# class CustomerSerializer(serializers.ModelSerializer):
#     orders = OrderSerializer(many=True, read_only=True, source='order')
#     class Meta:
#         model = Customers
#         fields = '__all__'




# class CustomerSerializer(serializers.ModelSerializer):
#     customer = OrderItemSerializer(many=True, read_only=True)  
#     class Meta:
#         model = Customers
#         fields = '__all__'


 
class CustomerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True, source='order')
    order_count = serializers.SerializerMethodField()
    country = shipping_CountrySerializer()   
    class Meta:
        model = Customers
        fields = '__all__'

    def get_order_count(self, obj):
        # Returns the count of orders related to the customer
        return obj.order.count()


class Customers_Serializer(serializers.ModelSerializer):
    country = shipping_CountrySerializer()   
    order_count = serializers.SerializerMethodField()
    class Meta:
        model = Customers
        fields = '__all__'
    def get_order_count(self, obj):
        # Returns the count of orders related to the customer
        return obj.order.count()
  



class OrderDashSerializer(serializers.ModelSerializer):
    customer= Customers_Serializer()
    shipping_company = Shipping_CompanySerializer()  # Use shipping_company here instead of Shipping
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields ="__all__"
    def get_order_count(self, obj):
        # Returns the count of orders related to the customer
        return obj.order.count()