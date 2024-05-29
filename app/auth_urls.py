

from app.auth_api import *
from django.urls import path




urlpatterns = [

    path('register/', registration_view, name='register'),
    path('login/', login_view, name='mobile-login'),
    path('login-employee/', login_employee, name='login-employee'), 
    path('generate_otp/', generate_otp, name='generate_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('reset_confirm/', reset_confirm, name='reset_confirm'),
    path('logintoken/',login_with_token_and_pin, name='login_with_token_and_pin'),
]