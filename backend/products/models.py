from django.db import models
# from content.models import Page

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="files/images/Category/%Y/%m/%d/", blank=True, null=True)
    # name_ar = models.CharField(max_length=255)
    # name_en = models.CharField(max_length=255)
    # page = models.ForeignKey(Page, related_name='category', on_delete=models.CASCADE)
 

class Image_Product(models.Model):
    image = models.FileField(upload_to="files/images_Product/Item/%Y/%m/%d/", blank=True, null=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)



class Product(models.Model):
    Themes_TYPES = (
        ('classic', 'Classic'),
        ('simple', 'Simple'),
        ('modern', 'Modern'),
    )
    themes_desktop_Types = models.CharField(max_length=20, choices=Themes_TYPES , default="Classic")
    themes_tablet_Types = models.CharField(max_length=20, choices=Themes_TYPES , default="Classic")
    themes_mobile_Types = models.CharField(max_length=20, choices=Themes_TYPES , default="Classic")
    is_mobile = models.BooleanField(default=True)
    is_tablet = models.BooleanField(default=True)
    is_desktop = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=2, choices=[('ar', 'ar'),('en', 'en') ], default='ar')
    name = models.CharField(max_length=255)
    ssku = models.CharField(max_length=255, blank=True, null=True)


    description = models.TextField()
    details= models.TextField()
    price = models.IntegerField(default=0)
    # models.DecimalField(max_digits=10, decimal_places=2)

    discount  = models.IntegerField(default=0)
    stock = models.IntegerField()
    cost = models.IntegerField(default=0)
    # models.DecimalField(max_digits=10, decimal_places=2,default=0)
    stock_alarm = models.IntegerField(default=0)
    expiration_date_offer= models.DateField(blank=True, null=True)

    is_active_note = models.BooleanField(default=True)

    default_option = models.FloatField(default=0,blank=True, null=True)
    note_help_top = models.CharField(max_length=500, blank=True, null=True)
    note_help = models.CharField(max_length=500, blank=True, null=True)
    note_help_bottom = models.CharField(max_length=500, blank=True, null=True)
    
    is_active_cart = models.BooleanField(default=True)
    is_active_coupon  = models.BooleanField(default=True)
    image = models.ImageField(upload_to="files/images/products/%Y/%m/%d/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='product')

    # module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='product', null=True)
    images = models.ManyToManyField(Image_Product, blank=True, null=True)
 
    tags= models.TextField( blank=True, null=True)  
    
    class Meta:
        ordering = ['-date']
    
   

    def __str__(self):
        return self.name