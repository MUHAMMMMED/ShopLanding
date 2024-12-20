from django.db import models
from cart.models import Note
 
class Package(models.Model):
    image = models.FileField(upload_to="files/images/Item/%Y/%m/%d/", blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    stock_alarm = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.name} - {self.quantity} units'
    @property
    def is_empty(self):
        return self.quantity == 0

 
  
class Shipping_Company (models.Model):
    image = models.ImageField(upload_to="files/images/Item/%Y/%m/%d/", blank=True, null=True)
    name = models.CharField(max_length=50)
    shipping_price = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    work_days  = models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)
 

class shipping_Country (models.Model):
    name = models.CharField(max_length=50)
    tax  = models.IntegerField(default=0)
    Shipping = models.ManyToManyField(Shipping_Company, blank=True)

    def __str__(self):
        return str(self.name)
  
 
class Customers(models.Model):
    session_key = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15 )
    email  = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(shipping_Country, on_delete=models.CASCADE, blank=True, null=True)
    governorate = models.CharField(max_length=100 )
    city = models.CharField(max_length=100 )
    neighborhood= models.CharField(max_length=100 )
    street= models.CharField(max_length=100 )
    shipping_address = models.CharField(max_length=500, blank=True, null=True)
    purchase_count = models.PositiveIntegerField(default=0, blank=True, null=True) 
    total_spending = models.FloatField(default=0)
   
class Order(models.Model):
    
    # Shortened status codes for the database
    STATUS_CHOICES = [
        ('P', 'Placed'),
        ('PU', 'Pick-up'),
        ('Di', 'Dispatched'),
        ('PA', 'Package Arrived'),
        ('DFD', 'Dispatched for Delivery'),
        ('D', 'Delivery'),
        ('C', 'Cancel'),
    ]
    
    # Shortened day codes for the database
    DAY = [
        ('mon', 'الاثنين'),
        ('tue', 'الثلاثاء'),
        ('wed', 'الأربعاء'),
        ('thu', 'الخميس'),
        ('fri', 'الجمعة'),
        ('sat', 'السبت'),
        ('sun', 'الأحد'),
    ]
    
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    tax_amount = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    shipping = models.FloatField(default=0)
    tax = models.IntegerField(default=0)
    # note = models.TextField(blank=True, null=True)
    shipping_company = models.ForeignKey(Shipping_Company, on_delete=models.CASCADE, blank=True, null=True)
    anticipation = models.CharField(max_length=20, choices=DAY, blank=True, null=True)
    tracking = models.CharField(max_length=50, blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    paid = models.BooleanField(default=False)
    new = models.BooleanField(default=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='P')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='order', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.customer.name if self.customer else "No customer assigned"    

  
class DictionaryProductName (models.Model):
    name =  models.CharField(max_length=200)
    def __str__(self):
        return self.name
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    dictionary = models.ForeignKey(DictionaryProductName ,on_delete=models.CASCADE )
    quantity = models.PositiveIntegerField()
    price = models.IntegerField(default=0)
    notes = models.ManyToManyField(Note, blank=True)
    cost = models.IntegerField(default=0)
    date_sold = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    
 
