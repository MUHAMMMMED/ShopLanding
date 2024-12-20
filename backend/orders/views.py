from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from cart.models import *
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from .utils import get_price  
from rest_framework.permissions import IsAuthenticated
 

class OrdersViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer
  
class shipping_CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = shipping_Country.objects.all()
    serializer_class = shipping_CountrySerializer
  

class Shipping_CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shipping_Company.objects.all()
    serializer_class = Shipping_CompanySerializer
 
class shipping_CountryDash(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  
    queryset = shipping_Country.objects.all()
    serializer_class = shipping_CountrySerializer
  

class Shipping_CompanyDash(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Shipping_Company.objects.all()
    serializer_class = Shipping_CompanySerializer

    def create(self, request, *args, **kwargs):
        # Get the Country_id from the request data
        country_id = request.data.get('Country_id')
        if not country_id:
            return Response({"Country_id": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Add the Country_id to the serializer context
        serializer = self.get_serializer(data=request.data, context={'Country_id': country_id})
        if serializer.is_valid():
            # Save the new Shipping Company and return response
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
 
  
class ShippingAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        company_id = kwargs.get('id')   
        try:
            company = Shipping_Company.objects.get(id=company_id)
            serializer = Shipping_CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Shipping_Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

 

class Shipping_CompanyAPIView(APIView):
    def get(self, request, *args, **kwargs):
        country_id = kwargs.get('id')  
        try:
            country = shipping_Country.objects.get(id=country_id)
            serializer = shipping_CountrySerializer(country)
            data = serializer.data
            data['tax'] = country.tax
            return Response(data, status=status.HTTP_200_OK)
        except shipping_Country.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

  


 

class OrderAPIView(APIView):
    def post(self, request):
        try:
            # Step 1: Delete unpaid orders
            Order.objects.filter(paid=False).delete()
            # print('Step 1: Deleted unpaid orders')

            # Step 2: Validate cart ID
            cart_id = request.data.get("cartId")
            if not cart_id:
                return Response({"error": "Cart ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            cart = Cart.objects.filter(id=cart_id).first()
            if not cart:
                return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
            # print(f'Step 2: Validated Cart ID {cart_id}')

            name = request.data.get("name")
            phone = request.data.get("phone")
            governorate = request.data.get("governorate")
            city = request.data.get("city")
            neighborhood = request.data.get("neighborhood")
            street = request.data.get("street")
            country_id = request.data.get("country")
            shipping_id = request.data.get("Shipping")
           
            # Check if any required field is missing
            if not all([name, phone, governorate, city, neighborhood, street, country_id,shipping_id]):
                return Response({"error": "All fields (name, phone, governorate, city, neighborhood, street, country) are required"}, 
                                 status=status.HTTP_400_BAD_REQUEST)

            try:
                country = shipping_Country.objects.get(id=country_id)
            except shipping_Country.DoesNotExist:
                return Response({"error": "Shipping country not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Step 4: Fetch or create customer
            session_key = cart.session_id
            customer, created = Customers.objects.get_or_create(session_key=session_key)
            if not created:
                customer.name =  name
                customer.phone = phone
                customer.country = country
                customer.governorate = governorate
                customer.city = city
                customer.neighborhood = neighborhood
                customer.street = street
                customer.save()
            # print(f'Step 4: Customer {"created" if created else "updated"}')

            # Step 5: Validate and fetch shipping company
            shipping_id = request.data.get("Shipping")
            if not shipping_id:
                return Response({"error": "Shipping ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            shipping_company = Shipping_Company.objects.filter(id=shipping_id).first()
            if not shipping_company:
                return Response({"error": "Shipping company not found"}, status=status.HTTP_404_NOT_FOUND)
            # print(f'Step 5: Validated Shipping Company ID {shipping_id}')

            # Step 6: Create order
            order = Order.objects.create(
                session_key=cart.session_id,
                customer = customer,
                shipping_company=shipping_company,
                shipping=shipping_company.shipping_price
            )
            
            # Step 7: Add items to the order
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
            # print('Step 7: Added cart items to the order')

            # Store Order ID in session
            request.session['order_id'] = order.id
            # print(f'Session updated with order ID {order.id}')

            return Response({"orderId": order.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 
 
class UpdateStatus(APIView):
    permission_classes = [IsAuthenticated]  

    def put(self, request, pk):
        status_param = request.query_params.get('status')
        if not status_param:
            return Response({"error": "Status parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        order.status = status_param
        order.save()
        return Response({"message": "Status updated successfully"}, status=status.HTTP_200_OK)



 
class UpdateAnticipation(APIView):
    permission_classes = [IsAuthenticated]  

    def put(self, request, pk):
        anticipation_param = request.query_params.get('anticipation')
        if not anticipation_param:
            return Response({"error": "anticipation parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        order.anticipation = anticipation_param
        order.save()
        return Response({"message": "anticipation updated successfully"}, status=status.HTTP_200_OK)


class UpdatePackage(APIView):
    permission_classes = [IsAuthenticated]  

    def put(self, request, pk):
        package_param = request.query_params.get('package')
     
        if not package_param:
            return Response({"error": "package parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            package = Package.objects.get(pk=package_param)
        except Package.DoesNotExist:
            return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)
        order.package = package
        order.save()
        return Response({"message": "Package updated successfully"}, status=status.HTTP_200_OK)




class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the 'new' attribute of the order if it's True
        if order.new:
            order.new = False
            order.save()  # Save the order after updating

        # Fetching all order items related to the order
        order_items = OrderItem.objects.filter(order_id=order.id)
        
        # Count the number of items in the cart
        cart_items_count = order_items.count()

        # Calculate total quantity of items in the order
        cart_quantity = sum(item.quantity for item in order_items)

        # Serialize the order and order items
        serializer = OrderDashSerializer(order)
      
        # Construct response data
        data = serializer.data
        data['cart_quantity'] = cart_quantity
        data['cart_items_count'] = cart_items_count

        return Response(data, status=status.HTTP_200_OK)

 
class DeleteOrder(APIView):
    permission_classes = [IsAuthenticated] 
    def delete(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs.get('pk') )  
        try:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR )
           

  

class InvoiceDetail(APIView):

    def get(self, request, *args, **kwargs):
        # order_id = kwargs.get('pk')
        session_id = request.session.session_key

        try:
            # Fetch the order instance
            order = Order.objects.get(session_key=session_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all order items related to the order
        order_items = OrderItem.objects.filter(order_id=order.id)

        # Count the number of items in the cart
        cart_items_count = order_items.count()

        # Calculate total quantity of items in the order
        cart_quantity = sum(item.quantity for item in order_items)

        # Serialize the order and order items
        serializer = OrderDashSerializer(order)
        order_item_serializer = OrderItemSerializer(order_items, many=True)

        # Construct response data
        data = serializer.data
        data['items'] = order_item_serializer.data
        data['cart_quantity'] = cart_quantity
        data['cart_items_count'] = cart_items_count

        return Response(data, status=status.HTTP_200_OK)


 