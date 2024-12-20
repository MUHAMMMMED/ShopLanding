from django.db import models
import uuid   
from products.models import  *
from visitors.models import Campaign ,Source , Medium
 
class Page(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField( blank=True, null=True) 
    keywords= models.TextField( blank=True, null=True)  
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.title
  
class Links(models.Model):
    page = models.ForeignKey(Page, related_name='Link', on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='Link', blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='Link', blank=True, null=True)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE, related_name='Link', blank=True, null=True)
   
    def __str__(self):
        return f"Link for Page: {self.page.title}"

 

class Settings(models.Model):
    home = models.ForeignKey(Page, related_name='home_settings', on_delete=models.CASCADE,blank=True, null=True)
    about = models.ForeignKey(Page, related_name='about_settings', on_delete=models.CASCADE,blank=True, null=True)
    privacy = models.ForeignKey(Page, related_name='privacy_settings', on_delete=models.CASCADE,blank=True, null=True)
    contactUs = models.ForeignKey(Page, related_name='contactUs_settings', on_delete=models.CASCADE,blank=True, null=True)
    currency_ar= models.CharField(max_length= 50 ,blank=True, null=True)
    currency_en= models.CharField(max_length= 50 ,blank=True, null=True)




# class PagesStore(models.Model):
#     home = models.OneToOneField(Page, related_name='home_store', on_delete=models.CASCADE)
#     about = models.OneToOneField(Page, related_name='about_store', on_delete=models.CASCADE)
#     privacy = models.OneToOneField(Page, related_name='privacy_store', on_delete=models.CASCADE)
#     contactUs = models.OneToOneField(Page, related_name='contact_store', on_delete=models.CASCADE)


 
# class Home(models.Model):
#     title = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=False)
#     page = models.ForeignKey(Page, related_name='home', on_delete=models.CASCADE)
#     def save(self, *args, **kwargs):
#         # Ensure only one instance is active
#         if self.is_active:
#             Home.objects.filter(is_active=True).update(is_active=False)
#         super(Home, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.title
    
    


# class About(models.Model):
#     title = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=False)
#     page = models.ForeignKey(Page, related_name='about', on_delete=models.CASCADE)
#     def save(self, *args, **kwargs):
#         # Ensure only one instance is active
#         if self.is_active:
#             About.objects.filter(is_active=True).update(is_active=False)
#         super(About, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.title
     

# class PrivacyPolicy(models.Model):
#     title = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=False)
#     page = models.ForeignKey(Page, related_name='privacy', on_delete=models.CASCADE)
#     def save(self, *args, **kwargs):
#         # Ensure only one instance is active
#         if self.is_active:
#             PrivacyPolicy.objects.filter(is_active=True).update(is_active=False)
#         super(PrivacyPolicy, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.title
    


 
# class ContactUs(models.Model):
#     title = models.CharField(max_length=100)
#     # email = models.EmailField()
#     # message = models.TextField()
#     is_active = models.BooleanField(default=False)
#     page = models.ForeignKey(Page, related_name='contactUs', on_delete=models.CASCADE)
#     def save(self, *args, **kwargs):
#         # Ensure only one instance is active
#         if self.is_active:
#             ContactUs.objects.filter(is_active=True).update(is_active=False)
#         super(ContactUs, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.title
    

 


class Section(models.Model):
    page = models.ForeignKey(Page, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # order = models.PositiveIntegerField(default=0)   
    mobile_order = models.PositiveIntegerField(default=0)   
    tablet_order = models.PositiveIntegerField(default=0)   
    desktop_order = models.PositiveIntegerField(default=0)   
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  

    def __str__(self):
        return self.title
     
    


 
  
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    def __str__(self):
        return self.name
 
class HeaderModule(models.Model):

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
    # module = models.OneToOneField(Module, on_delete=models.CASCADE, related_name='header')
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    menu_items = models.ManyToManyField(MenuItem, related_name='headers')



class SliderModule(models.Model):

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
    images = models.ImageField(upload_to='sliders/')


class ContentModule(models.Model):

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
    text = models.TextField()


class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    def __str__(self):
        return self.platform

class FooterModule(models.Model):
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
    content = models.TextField()
    copyright_text = models.CharField(max_length=100)
    social_links = models.ManyToManyField(SocialLink, related_name='footers')

 

class Module(models.Model):
    MODULE_TYPES = (
        ('header', 'Header'),
        ('slider', 'Slider'),
        ('content', 'Content'),
        ('product', 'Product'),
        ('footer', 'Footer'),
    )
    section = models.ForeignKey(Section, related_name='modules', on_delete=models.CASCADE)
    module_type = models.CharField(max_length=20, choices=MODULE_TYPES , default="header")  
    mobile_order = models.PositiveIntegerField(default=0)   
    tablet_order = models.PositiveIntegerField(default=0)   
    desktop_order = models.PositiveIntegerField(default=0)   
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) 
    header = models.ForeignKey(HeaderModule, on_delete=models.CASCADE, related_name='module', blank=True, null=True)
    slider = models.ForeignKey(SliderModule, on_delete=models.CASCADE, related_name='module', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='module', blank=True, null=True)
    content = models.ForeignKey(ContentModule, on_delete=models.CASCADE, related_name='module', blank=True, null=True)
    footer = models.ForeignKey(FooterModule, on_delete=models.CASCADE, related_name='module', blank=True, null=True)


   




 
# class SiteStyle(models.Model):
#     primary_color = models.CharField(max_length=7, default="#3498db")
#     secondary_color = models.CharField(max_length=7, default="#2ecc71")
#     background_color = models.CharField(max_length=7, default="#f5f5f5")
#     text_color = models.CharField(max_length=7, default="#333333")
#     font_family = models.CharField(max_length=100, default="Arial, sans-serif")
#     box_shadow = models.CharField(max_length=100, default="0px 4px 6px rgba(0, 0, 0, 0.1)")
#     border_radius = models.CharField(max_length=10, default="5px")
#     border_color = models.CharField(max_length=7, default="#dddddd")

#     def __str__(self):
#         return "Site Style Configuration"

 

# class Theme(models.Model):
#     name = models.CharField(max_length=100)
#     primary_color = models.CharField(max_length=7, default="#3498db")
#     secondary_color = models.CharField(max_length=7, default="#2ecc71")
#     background_color = models.CharField(max_length=7, default="#ffffff")
#     text_color = models.CharField(max_length=7, default="#333333")

#     def __str__(self):
#         return self.name
    