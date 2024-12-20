
from decimal import Decimal

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from cart.models import *
from .models import *
from .serializers import *

def get_price(product):
    # تحويل discount و price إلى Decimal لضمان التوافق في العمليات الحسابية
    discount = Decimal(product.discount) if isinstance(product.discount, (int, float)) else product.discount
    price = Decimal(product.price) if isinstance(product.price, (int, float)) else product.price
    
    if discount <= 0:
        return price
    else:
        # الآن العملية الحسابية تتم بين قيم من نفس النوع (Decimal)
        price = price - (price * (discount / Decimal(100)))  # التأكد من أن القسمة تتم على Decimal
        return price
 


def validate_cart(self, cart_id):
        """
        Validate the provided cart ID.
        """
        if not cart_id:
            return Response({"error": "Cart ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        return cart





def delete_unpaid_orders(self):
        """
        Delete all unpaid orders.
        """
        Order.objects.filter(paid=False).delete()
 

  
def validate_customer_data(self, request_data):
        """
        Validate the customer data such as name, phone, address fields.
        """
        required_fields = ["name", "phone", "country", "governorate", "city", "neighborhood", "street", "country_id"]
        
        for field in required_fields:
            if not request_data.get(field):
                return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        return None  # No errors

def get_shipping_country(self, country_id):
        """
        Fetch shipping country by its ID.
        """
        try:
            return shipping_Country.objects.get(id=country_id)
        except shipping_Country.DoesNotExist:
            return None

def get_or_create_customer(self, session_key, customer_data):
        """
        Get or create customer based on session key and provided data.
        """
        customer, created = Customers.objects.get_or_create(session_key=session_key)
        if not created:
            customer.name = customer_data['name']
            customer.phone = customer_data['phone']
            customer.country = customer_data['country']
            customer.governorate = customer_data['governorate']
            customer.city = customer_data['city']
            customer.neighborhood = customer_data['neighborhood']
            customer.street = customer_data['street']
            customer.save()
        return customer

def validate_shipping_company(self, shipping_id):
        """
        Validate and fetch shipping company by ID.
        """
        if not shipping_id:
            return None

        shipping_company = Shipping_Company.objects.filter(id=shipping_id).first()
        if not shipping_company:
            return None
        
        return shipping_company

def create_order(self, cart, customer, shipping_company):
        """
        Create an order using the cart, customer, and shipping company.
        """
        return Order.objects.create(
            session_key=cart.session_id,
            customer=customer,
            shipping_company=shipping_company
        )

def add_cart_items_to_order(self, cart, order):
        """
        Add items from the cart to the created order.
        """
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error": "No items found in the cart"}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            dictionary, _ = DictionaryProductName.objects.get_or_create(name=item.product.name)
            order_item = OrderItem.objects.create(
                order=order,
                dictionary=dictionary,
                quantity=item.quantity,
                price=item.product.price,
                cost=item.product.cost,
            )
            order_item.notes.set(item.notes.all())
            order_item.save()
