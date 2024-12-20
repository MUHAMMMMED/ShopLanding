from user_agents import parse
from django.utils.crypto import get_random_string
from geoip2.database import Reader
from django.conf import settings
import logging
import hashlib
import os
from .models import *
from django.db.models import Q
from django.utils import timezone
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.http import JsonResponse
 
logger = logging.getLogger(__name__)

from faker import Faker
import random

# إنشاء كائن faker
fake = Faker()
# قائمة موسعة من رموز ISO للدول لتوليد IPs منها
country_codes = [
    'US', 'CA', 'GB', 'FR', 'DE', 'IT', 'ES', 'JP', 'CN', 'IN',
    'BR', 'RU', 'AU', 'ZA', 'EG', 'SA', 'AE', 'KR', 'TR', 'MX',
    'AR', 'CL', 'NL', 'SE', 'NO', 'FI', 'DK', 'PL', 'PT', 'GR',
    'BE', 'AT', 'CH', 'IE', 'NZ', 'SG', 'MY', 'TH', 'VN', 'PH'
]


def generate_random_ip():
    """
    هذه الدالة تختار دولة عشوائيًا من قائمة الدول وتقوم بتوليد IP مرتبط بهذه الدولة.
    """
    # اختيار دولة عشوائيًا من قائمة رموز الدول
    selected_country = random.choice(country_codes)
    # توليد عنوان IP عشوائي
    ip_address = fake.ipv4_public()
    return {
        'ip_address': ip_address,
        'country': selected_country
    }

# مثال على الاستخدام
generated_ip_info = generate_random_ip()
print(f"Generated IP: {generated_ip_info['ip_address']} in Country: {generated_ip_info['country']}")
 

 
# def home(request):
# def record_visit(request, product_id=None):
#     # استدعاء دالة لتسجيل زيارة الصفحة الرئيسية
#     response = register_visit(request, product_id=None)  # لا يوجد product_id هنا
#     response = register_visit(request, product_id)  # تمرير product_id
    # register_visit(request, skip=True)  # يتم تخطي التسجيل
#     return response

  
 
def register_visit(request, product_id):
    # التحقق من التوكن في الهيدر
    token = request.headers.get('Authorization', '').replace('Token ', '')
    if token == 'skip':
        # إذا كان التوكن يحتوي على "skip"، نعود برسالة توضح أن التسجيل تم تخطيه
        return JsonResponse({"message": "User opted out of tracking."})

    today = datetime.now().date()
    cookie_name = f'visit_{product_id}' if product_id else 'visit_Default'
    last_visit_date = request.COOKIES.get(cookie_name)

    if last_visit_date == str(today):
        return JsonResponse({"message": "Visit already recorded for today."})

    visitor_data = RecordVisitor(request)
    response = JsonResponse(visitor_data)
    response.set_cookie(cookie_name, str(today))

    return response

 






# def register_visit(request, product_id=None):
#     # التحقق من التوكين من جانب الواجهة
#     consent_token = request.COOKIES.get('cookie_token')
#     if consent_token == 'skip':
#         # إذا كان التوكين skip، نوقف عملية تسجيل البيانات
#         return {"message": "Data collection skipped due to user choice."}
    
#     today = datetime.now().date()
    
#     # التحقق مما إذا كانت الزيارة سجلت لهذا اليوم
#     last_visit_date = request.COOKIES.get(f'last_visit_date_{product_id or "default"}')
#     if last_visit_date == str(today):
#         return {"message": "Visit already recorded for today."}

#     # تسجيل الزيارة لأن المستخدم وافق على الكوكيز
#     visitor_data = RecordVisitor(request)

#     # إعداد رد وتحديث الكوكي بتاريخ اليوم للصفحة أو المنتج المحدد
#     response = JsonResponse(visitor_data)
#     response.set_cookie(f'last_visit_date_{product_id or "default"}', str(today))
#     return response

 



# Generate a salt value for hashing IPs
def generate_salt(length=16):
    return os.urandom(length).hex()


# Hash the IP address with a salt for privacy
def hash_ip(ip, salt):
    return hashlib.sha256((ip + salt).encode('utf-8')).hexdigest()


# Get the client's IP address from request headers
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip

 

# Create a browser fingerprint using the User-Agent and IP address
def get_browser_fingerprint(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ip_address = get_client_ip(request)
    fingerprint_data = f"{user_agent}-{ip_address}".encode('utf-8')
    return hashlib.sha256(fingerprint_data).hexdigest()





# Retrieve device information, such as device type, OS family, and browser
def get_device_info(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    device_type = 'Desktop' if user_agent.is_pc else 'Mobile' if user_agent.is_mobile else 'Tablet'
    os_family = user_agent.os.family
    browser = user_agent.browser.family
    return device_type, os_family, browser

 

 

from geoip2.database import Reader
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_geo_info(ip_address, hashed_ip, salt):
    geo_info = {}  # Initialize geo_info to avoid UnboundLocalError
    try:
        with Reader(settings.GEOIP_PATH) as reader:
            response = reader.city(ip_address)
            geo_info = {
                'ip_address': ip_address,
                'hashed_ip': hashed_ip,
                'salt': salt,
                'region': response.continent.name,
                'country': response.country.name,
                'state': response.subdivisions.most_specific.name,
                'city': response.city.name,
                # Uncomment below as needed
                # 'country_iso_code': response.country.iso_code,
                # 'state_iso_code': response.subdivisions.most_specific.iso_code,
                # 'postal_code': response.postal.code,
                # 'latitude': response.location.latitude,
                # 'longitude': response.location.longitude,
                # 'timezone': response.location.time_zone,
                # 'continent_iso_code': response.continent.code,
            }
    except Exception as e:
        logger.error(f"GeoIP lookup failed for IP {ip_address}: {e}")
        geo_info = {'error': str(e)}
    return geo_info
 

 


# Extract UTM parameters from the request URL and store them in session
def get_utm_parameters(request):
    utm_source = request.GET.get('utm_source')
    utm_medium = request.GET.get('utm_medium')
    utm_campaign = request.GET.get('utm_campaign')
    if utm_source:
        request.session['utm_source'] = utm_source
        request.session['utm_medium'] = utm_medium
        request.session['utm_campaign'] = utm_campaign
    return utm_source, utm_medium, utm_campaign

 
 

 


def create_new_visitor(visitor_data):
    try:
        device, _ = Device.objects.get_or_create(name=visitor_data.get('device_type', 'Unknown Device'))
        os_family, _ = OperatingSystem.objects.get_or_create(name=visitor_data.get('os_family', 'Unknown OS'))
        browser, _ = Browser.objects.get_or_create(name=visitor_data.get('browser', 'Unknown Browser'))

        # Check and create PlaceDictionary entries only if the data is available
        if visitor_data.get('region'):
            place_name_region, _ = PlaceDictionary.objects.get_or_create(name=visitor_data['region'])
            region, _ = Region.objects.get_or_create(place_name=place_name_region)
        else:
            region = None

        if visitor_data.get('country'):
            place_name_country, _ = PlaceDictionary.objects.get_or_create(name=visitor_data['country'])
            country, _ = Country.objects.get_or_create(place_name=place_name_country)
        else:
            country = None

        if visitor_data.get('state') and country:
            place_name_state, _ = PlaceDictionary.objects.get_or_create(name=visitor_data['state'])
            state, _ = State.objects.get_or_create(place_name=place_name_state, country=country)
        else:
            state = None

        if visitor_data.get('city') and state:
            place_name_city, _ = PlaceDictionary.objects.get_or_create(name=visitor_data['city'])
            city, _ = City.objects.get_or_create(place_name=place_name_city, state=state)
        else:
            city = None

        date, _ = Date.objects.get_or_create(date=timezone.now().date())

        # Create the new UserVisit record
        user=UserVisit.objects.create(
            hashed_ip=visitor_data['hashed_ip'],
            salt=visitor_data['salt'],
            browser_fingerprint=visitor_data['browser_fingerprint'],
            user_cookie=visitor_data['user_cookie'],
            device_type=device,
            operating_system=os_family,
            browser=browser,
            region=region,
            country=country,
            created_at=date,
        )
        return user.id

    except IntegrityError as e:
        print(f"IntegrityError while creating UserVisit: {e}")
    except Exception as e:
        print(f"An error occurred while creating UserVisit: {e}")
    return None  # Return None if creation failed
 

def update_visitor(stored_visit, visitor_data):
    # Helper function to safely retrieve or create PlaceDictionary entries
    def get_or_create_place(name):
        if name:
            place, _ = PlaceDictionary.objects.get_or_create(name=name)
            return place
        return None  # Return None if name is None or empty

    # Retrieve or create device, OS, and browser instances
    device, _ = Device.objects.get_or_create(name=visitor_data.get('device_type', 'Unknown'))
    os_family, _ = OperatingSystem.objects.get_or_create(name=visitor_data.get('os_family', 'Unknown'))
    browser, _ = Browser.objects.get_or_create(name=visitor_data.get('browser', 'Unknown'))

    # Get or create region, country, state, and city details with checks for empty values
    place_name_region = get_or_create_place(visitor_data.get('region'))
    region = Region.objects.get_or_create(place_name=place_name_region)[0] if place_name_region else None
    
    place_name_country = get_or_create_place(visitor_data.get('country'))
    country = Country.objects.get_or_create(place_name=place_name_country)[0] if place_name_country else None
    
    place_name_state = get_or_create_place(visitor_data.get('state'))
    state = State.objects.get_or_create(place_name=place_name_state, country=country)[0] if place_name_state else None
    
    place_name_city = get_or_create_place(visitor_data.get('city'))
    city = City.objects.get_or_create(place_name=place_name_city, state=state)[0] if place_name_city else None

    # Update visitor information
    stored_visit.hashed_ip = visitor_data.get('hashed_ip')
    stored_visit.browser_fingerprint = visitor_data.get('browser_fingerprint')
    stored_visit.user_cookie = visitor_data.get('user_cookie')
    stored_visit.device_type = device
    stored_visit.operating_system = os_family
    stored_visit.browser = browser
    stored_visit.region = region if region else stored_visit.region  # Set region only if not None
    stored_visit.country = country if country else stored_visit.country  # Set country only if not None

    # Increment the total visit count for returning visitors
    stored_visit.total_visits = stored_visit.total_visits + 1
    # Save updated information
    stored_visit.save()

    return stored_visit.id 


 


def calculate_score(stored_visit, visitor_data):
    salt = stored_visit.salt
    hashed_ip = hash_ip(visitor_data['ip_address'], salt)
    state = State.objects.filter(country=stored_visit.country)
    score = 0

    if visitor_data['browser_fingerprint'] == stored_visit.browser_fingerprint:
        score += 1
    if visitor_data['user_cookie'] == stored_visit.user_cookie:
        score += 1
    if visitor_data['device_type'] == stored_visit.device_type.name:
        score += 1
    if visitor_data['os_family'] == stored_visit.operating_system.name:
        score += 1
    if visitor_data['country'] == stored_visit.country.place_name.name:
        score += 1
    if visitor_data['state'] == state:
        score += 1
    if visitor_data['hashed_ip'] == hashed_ip:
        score += 1

    return score


 

def Hourly_Visit(userID, visitor_data):
    try:
        user = UserVisit.objects.get(id=userID)

        # Retrieve or create dictionaries and link them
        source, _ = SourceDictionary.objects.get_or_create(name=visitor_data['Coming_from'])
        medium, _ = MediumDictionary.objects.get_or_create(name=visitor_data['Advertising_Platform'])
        campaign, _ = CampaignDictionary.objects.get_or_create(name=visitor_data['Coming_from'])

        # Create instances
        source_entry, _ = Source.objects.get_or_create(dictionary_source=source)
        medium_entry, _ = Medium.objects.get_or_create(dictionary_medium=medium)
        campaign_entry, _ = Campaign.objects.get_or_create(dictionary_campaign=campaign)

        # Get the current time rounded to the nearest hour
        current_time = timezone.now()
        rounded_hour = current_time.replace(minute=0, second=0, microsecond=0)
        
        hour, _ = Hour.objects.get_or_create(hour=rounded_hour.hour)
        date, _ = Date.objects.get_or_create(date=rounded_hour.date())

        # Check if an HourlyVisit entry already exists for this user, date, and hour
        if not HourlyVisit.objects.filter(user_visit=user, date=date, hour=hour).exists():
            # Create a new HourlyVisit entry if no existing record is found
            HourlyVisit.objects.create(
                user_visit=user,
                date=date,
                source=source_entry,
                medium=medium_entry,
                campaign=campaign_entry,
                hour=hour,
            )
        else:
            print(f"Hourly visit already exists for user {userID} on {date} at hour {hour}.")

    except UserVisit.DoesNotExist:
        print(f"UserVisit with id {userID} does not exist.")
    except Exception as e:
        print(f"Error in Hourly_Visit: {e}")







 

def check_visitor(visitor_data, threshold=1):
    """
    Check if the visitor is known based on their data.
    If known, update their information; otherwise, add them as a new visitor.
    """
    user_visits = UserVisit.objects.filter(
        Q(hashed_ip=visitor_data['hashed_ip']) |
        Q(browser_fingerprint=visitor_data['browser_fingerprint']) |
        Q(user_cookie=visitor_data['user_cookie']) |
        Q(device_type__name=visitor_data['device_type']) |
        Q(operating_system__name=visitor_data['os_family']) |
        Q(country__place_name__name=visitor_data['country'])
    )

    # Check existing visits and calculate matching points
    for stored_visit in user_visits:
        score = calculate_score(stored_visit, visitor_data)

        if score >= threshold:
            userID = update_visitor(stored_visit, visitor_data)
            Hourly_Visit(userID, visitor_data)
            return "The visitor is recognized and has been updated with new information."
    
    # If not recognized, create a new record
    userID = create_new_visitor(visitor_data)
    Hourly_Visit(userID, visitor_data)
    return "The visitor is new and has been recorded."

 



def RecordVisitor(request):
    # Get device and browser information
    device_type, os_family, browser = get_device_info(request)
    
    # Retrieve the IP address and generate salt and hashed IP
    # ip_address = '66.242.64.1'  # For testing, replace with `get_client_ip(request)` in production
    visitor_ip_info = generate_random_ip()  # احصل على تفاصيل الزائر
    ip_address = visitor_ip_info['ip_address']
   
    salt = generate_salt()
    hashed_ip = hash_ip(ip_address, salt)
    
    # Create a unique browser fingerprint
    browser_fingerprint = get_browser_fingerprint(request)
    
    # Set up user cookie if not already present
    user_cookie = request.COOKIES.get('user_cookie', get_random_string(32))
    
    # Get geographic information using GeoIP
    geo_info = get_geo_info(ip_address, hashed_ip, salt)
    
    # Retrieve UTM parameters if available
    utm_source, utm_medium, utm_campaign = get_utm_parameters(request)

    # Visitor data dictionary
    visitor_data = {
        'ip_address': ip_address,
        'hashed_ip': hashed_ip,
        'salt': salt,
        'device_type': device_type,
        'os_family': os_family,
        'browser': browser,
        'browser_fingerprint': browser_fingerprint,
        'user_cookie': user_cookie,
        'region': geo_info['region'], 
        'country': geo_info['country'],  
        'state': geo_info['state'],   
        'city': geo_info['city'],   

        # 'country_iso_code': geo_info['country_iso_code'], 
        # 'state_iso_code': geo_info['state_iso_code'], 
        # 'postal_code': geo_info['postal_code'],  
        # 'latitude': geo_info['latitude'],   
        # 'longitude': geo_info['longitude'],  
        # 'timezone': geo_info['timezone'],   
        # 'continent': geo_info['continent'],  
        # 'continent_iso_code': geo_info['continent_iso_code'],  
        'Coming_from': utm_source,
        'Advertising_Platform': utm_medium,
        'Campaign_Name': utm_campaign,
    }
 
    # is_returning = is_returning_visitor(visitor_data) 
    is_returning = check_visitor(visitor_data, threshold=3) 
    # Return a dictionary containing all collected data
    return {'visitor_data': visitor_data, 'is_returning': is_returning }

    # return  geo_info







 