from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse 
from django.http import JsonResponse
from rest_framework.request import Request
from django.utils.encoding import smart_str
from django.conf import settings
from orders.models import Order,OrderItem
from cart.models import Cart 
import json
import stripe
import logging
from .utils import *
  
DOMAIN =settings.DOMAIN
 
 

# Set the Stripe API key
stripe.api_key = 'sk_test_51M0Bs9A9gttpg3uSGA5xQhMRCLgEaywkUYXphiJv5oT9MbDOTvNocMgzpfWu9fpvBira9Jiv4sKpIyGPX4XSq5tL00VCMwZq91'

STRIPE_WEBHOOK_SECRET='whsec_583c87d69ea6c87e5c56ec19dac24ae51887a3cb70f75b67226e24921192aa9f'

DOMAIN =settings.DOMAIN
 
# Set the Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

 


# Configure logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_checkout_session(request: Request):
    try:
        data = request.data  # This will parse the request body as JSON
        items = data.get('items')
        if not items:
            return JsonResponse({'error': 'Items list is missing'}, status=400)

        line_items = []
        for item in items:
            order_id = item.get('id')
            cart_id = item.get('cart_id')
            final_total = item.get('Total')
            taxAmount = item.get('taxAmount')
            session_id = request.session.session_key or request.session.save()
         
            handle_Cart_To_OrderItem(final_total,taxAmount,order_id, cart_id) 
 
            if not order_id or not final_total:
                return JsonResponse({'error': 'Order ID or final total is missing in one of the items'}, status=400)

            # Convert final_total to the smallest currency unit (cents)
            final_total_cents = int(float(final_total) * 100)

            line_items.append({
                'price_data': {
                    'currency': 'SAR',
                    'product_data': {
                        'name': 'اجمالي المدفوعات',
                    },
                    'unit_amount': final_total_cents,
                },
                'quantity': 1,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{DOMAIN}/success',
            # success_url=f'http://localhost:3000/success',
            
            cancel_url=f'{DOMAIN}/cancel',
            metadata={
                "session_id": session_id,
                "order_id": order_id,
                "cart_id":cart_id
            }
        )

        return JsonResponse({'url': checkout_session.url})

    except json.JSONDecodeError as e:
        logger.error(f'Invalid JSON: {str(e)}')
        return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)
    except stripe.error.StripeError as e:
        logger.error(f'Stripe error: {str(e)}')
        return JsonResponse({'error': f'Stripe error: {str(e)}'}, status=403)
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        return JsonResponse({'error': str(e)}, status=403)

 










 
@api_view(['POST'])
@csrf_exempt
def stripe_webhook(request):
   
    payload = smart_str(request.body)
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        logger.error("Invalid payload")
        return JsonResponse({'error': "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature")
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})
        order_id = metadata.get("order_id")
        cart_id = metadata.get("cart_id")
        email = session.get('customer_details', {}).get('email')

        # print(f"Session metadata: {metadata}")
   
        if not order_id:
            logger.error("Order ID or Session ID is missing in metadata.")
            return JsonResponse({"error": "Order ID or Session ID is missing in metadata."}, status=400)

        try:
            invoice_number = generate_invoice_number()
            tracking_number = generate_tracking_number()
            order = Order.objects.get(id=order_id)
            order.paid = True
            # order.session_key = ''
            order.invoice_number = invoice_number
            order.tracking = tracking_number
            order.save()

            # print(f"Order {order_id} updated successfully.")

            customer = order.customer
            if customer:
                customer.email = email
                customer.save()

            items = OrderItem.objects.filter(order_id=order_id)
            for item in items:
                item.paid = True
                item.save()

            cart = Cart.objects.get(id=cart_id)
            cart.delete()
            # print(f"Cart {cart_id} deleted successfully.")

        except Order.DoesNotExist:
            logger.error(f"Order with id {order_id} does not exist.")
            return JsonResponse({"error": f"Order with id {order_id} does not exist."}, status=404)
        except OrderItem.DoesNotExist:
            logger.error(f"No items found for order id {order_id}.")
            return JsonResponse({"error": f"No items found for order id {order_id}."}, status=404)
         
    return JsonResponse({"status": "success"})




 