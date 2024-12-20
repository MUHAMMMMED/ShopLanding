from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Cart, CartItem
from .serializers import *
from content.models import Product
from rest_framework.permissions import IsAuthenticated
from .utils import *
from rest_framework import viewsets
 
class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract the product ID, quantity, and notes from the request body
        product_id = request.data.get('productId')
        quantity = request.data.get('quantity', 1)  # Default quantity is 1 if not provided
        notes = request.data.get('notes', [])  # Notes are optional
 
        # Check if there is an existing session
        if request.session.session_key:
            session_id = request.session.session_key  # Get the current session ID

            # Check if this session is associated with any cart
            try:
                cart = Cart.objects.get(session_id=session_id)
            except Cart.DoesNotExist:
                cart = None  # If no cart is found, it means the session is not associated with any cart
            
            if cart is None:
                # If no cart is found for the current session, delete the session key if it exists
                if 'session_key' in request.session:
                    del request.session['session_key']
                request.session.create()  # Create a new session
                session_id = request.session.session_key  # Get the new session ID
        else:
            # If no session exists, create a new session
            request.session.create()
            session_id = request.session.session_key  # Get the new session ID

        try:
            # Retrieve the product from the database; return a 404 error if it does not exist
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a cart for this session if it does not already exist
        cart, _ = Cart.objects.get_or_create(session_id=session_id)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # If the cart item already exists, update the quantity
            cart_item.quantity += quantity

            # Retrieve existing notes for the cart item
            existing_notes = cart_item.notes.values_list('note', flat=True)

            # Add only the new notes that are not already present
            for note_text in notes:
                if note_text not in existing_notes:
                    note_data = {'note': note_text}  # Prepare the note data
                    note_serializer = NoteSerializer(data=note_data)  # Validate the note data
                    if note_serializer.is_valid():
                        # Save the new note and associate it with the cart item
                        note = note_serializer.save()
                        cart_item.notes.add(note)
                    else:
                        # If the note data is invalid, return a 400 Bad Request response
                        return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the cart item is new, set its quantity
            cart_item.quantity = quantity
            cart_item.save()

            # Add all provided notes to the new cart item
            for note_text in notes:
                note_data = {'note': note_text}  # Prepare the note data
                note_serializer = NoteSerializer(data=note_data)  # Validate the note data
                if note_serializer.is_valid():
                    # Save the new note and associate it with the cart item
                    note = note_serializer.save()
                    cart_item.notes.add(note)
                else:
                    # If the note data is invalid, return a 400 Bad Request response
                    return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save the cart item after adding/updating its quantity and notes
        cart_item.save()

        # Include the session_id in the response
        return Response({
            "message": "Product added/updated in cart",
            "session_id": session_id  # Include session ID for the frontend
        }, status=status.HTTP_200_OK)

 
class CartDetailView(APIView):
    def get(self, request, *args, **kwargs):
        session_id = request.session.session_key
        # Fetch the cart based on the session ID
        cart = get_object_or_404(Cart, session_id=session_id)

        cart_serializer = Cart_Serializer(cart)

        # Fetch the cart items with related product data
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        cart_items_count = cart_items.count()
        # currency = cart_items.first().product.currency 
        language = cart_items.first().product.language if cart_items.exists() else None
        currency = get_currency(language)
       
        # Serialize cart items
        serializer = CartItemSerializer(cart_items, many=True)

        # Calculate totals and cart quantity
        total, cart_quantity =  calculate_cart_totals(cart_items)

        # Prepare response data
        data = {
            'cart_data': cart_serializer.data,
            'cart_items': serializer.data,
            'cart_items_count': cart_items_count,
            'total': total,
            'cart_quantity': cart_quantity,
            'currency': currency
        }
        return Response(data, status=status.HTTP_200_OK)
  
 



 
class UpdateQuantityCartItemView(APIView):
    def put(self, request, *args, **kwargs):
        cart_item_id = kwargs.get('id')
        quantity = request.data.get('quantity', 1)
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()
        return Response({"message": "Cart item updated"}, status=status.HTTP_200_OK)


 
 
class DeleteCartItemView(APIView):
    def delete(self, request, *args, **kwargs):
        cart_item_id = kwargs.get('id')   
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        return Response({"message": "Cart item deleted"}, status=status.HTTP_200_OK)
 
 
class NoteCreateView(APIView):
    def post(self, request, id, format=None):
        try:
            cart_item = CartItem.objects.get(id=id)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            note = serializer.save()
            cart_item.notes.add(note)
            cart_item.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
class NoteUpdateView(APIView):
    def put(self, request, pk, format=None):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 

class ApplyCouponView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate request data
        code = request.data.get('code')
        total = request.data.get('Total')
        if not (code and total):
            return Response({'valid': False, 'error': 'Coupon code and total amount are required.'}, status=400)
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response({'valid': False, 'error': 'Invalid coupon code.'}, status=400)
        # Check coupon validity
        today = datetime.today().date()
        if coupon.expiryDate < today or coupon.coupon_usage <= 0:
            return Response({'valid': False, 'error': 'Invalid or expired coupon code.'}, status=400)
        # Calculate discounted price
        discounted_price = max(0, float(total) - (float(total) * coupon.discount / 100))
        # Update coupon usage
        coupon.coupon_usage -= 1
        coupon.save()

        return Response({'valid': True,'percentage':coupon.discount, 'discounted_price': discounted_price}, status=status.HTTP_200_OK)

 
class NoteListDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

    def get(self, request):
        notes = Note.objects.all()
        notes_count = notes.count()
        serializer = NoteSerializer(notes, many=True)
        data = {
            'notes': serializer.data,
            'notes_count': notes_count
        }
        return Response(data)
       

    def delete(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



 
class CouponViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
 