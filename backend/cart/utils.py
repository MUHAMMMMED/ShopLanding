from decimal import Decimal
from .serializers import *
 
def calculate_cart_totals( cart_items):
        total = Decimal(0)
        cart_quantity = 0

        for item in cart_items:
            quantity = item.quantity
            cart_quantity += quantity
            price = item.product.price
            discount = item.product.discount or 0  # Handle cases where discount might be None

            # Calculate the discount price
            discount_price = price - (price * Decimal(discount) / Decimal(100))
            subtotal = discount_price * quantity

            total += subtotal

        return total, cart_quantity



def get_currency(language):
    """Retrieve currency settings with a fallback for missing data."""
    settings = Settings.objects.first()  # Fetch the first settings record
    if settings:
        # Return one currency value as a string based on language preference
        if language == 'ar':
            return settings.currency_ar
        else:
            return settings.currency_en
    return ''  # Return an empty string if no settings are found
