from django.core.mail import EmailMessage
import random
from django.conf import settings
from .models import User, OneTimePassword
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from datetime import datetime
from .models import User, OneTimePassword 
from rest_framework.response import Response
from rest_framework import status   
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['full_name'] = user.get_full_name
    refresh['type'] = user.user_type
    # refresh['is_active'] = user.is_active
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
 
 


 
def send_generated_otp_to_email(email, request): 
    subject = "One time passcode for Email verification"
    otp = random.randint(1000, 9999)
    current_site = get_current_site(request).domain
    user = User.objects.get(email=email)

    # HTML email body
    email_body = render_to_string('otp_email_template.html', {
        'first_name': user.first_name,
        'current_site': current_site,
        'otp': otp,
        'current_year': datetime.now().year
    })

    from_email = settings.EMAIL_HOST_USER
    otp_obj = OneTimePassword.objects.create(user=user, otp=otp)
    
    # Send the email
    d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[user.email])
    d_email.content_subtype = 'html'  # This is necessary to send HTML email
    d_email.send()











 
def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()


# from django.core.mail import send_mail
# from django.http import HttpResponse
# from django.conf import settings

# def send_email(request):
#     subject = 'Test Email'
#     message = 'This is a test email sent from Django using Google SMTP.'
#     from_email = settings.EMAIL_HOST_USER  # Use the same email as EMAIL_HOST_USER
#     to_email = ['mohamedeg7000@gmail.com']  # Enter recipient email address(es)

#     send_mail(subject, message, from_email, to_email, fail_silently=False)
#     return HttpResponse('Email sent successfully!')



 
# def check_permissions(request):
#     """
#     Check if the user is authenticated and has permission to access the data.
#     """
#     if not request.user.is_authenticated:
#         return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

#     if request.user.user_type != 'M':  # Assuming 'M' represents the Manager user type
#         return Response({'error': 'You do not have permission to access this data.'}, status=status.HTTP_403_FORBIDDEN)
    
#     return None  # No error, user is authenticated and has permission
 

    # # Check permissions for the request
    # error_response = check_permissions(request)
    # if error_response:
    #     return error_response