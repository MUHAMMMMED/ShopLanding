from django.db import models
from content.models import Product



class Note(models.Model):
    note  = models.TextField()
    def __str__(self):
        return self.note

class Cart(models.Model):
    session_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.session_id
 
 
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField( null=True, blank=True )
    notes = models.ManyToManyField(Note, null=True, blank=True )
    def __str__(self):
        return self.cart.session_id

 
class Coupon(models.Model): 
    code = models.CharField(max_length=100)
    discount = models.FloatField(default=0,blank=True, null=True)
    coupon_usage= models.FloatField(default=0)
    expiryDate = models.DateField(blank=True, null=True)  
    def __str__(self):
        return self.code

 