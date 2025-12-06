
import string
import random
from .utils import *
from .models import *
from .serializer import *
from app.auth_ser import *
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404 ,render, redirect
from rest_framework.decorators import api_view, permission_classes

from .forms import *
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
# from .forms import PasswordResetRequestForm, SetPasswordForm
# from .forms import *
# from .models import *
# from .serializer import *
# from rest_framework import status
# from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import login,authenticate,logout
# from rest_framework.permissions import IsAuthenticated ,AllowAny
# from django.shortcuts import render, redirect, get_object_or_404
# from rest_framework.decorators import api_view, permission_classes

from django.conf import settings

message_server_error = "message sending error"
message_server_error_status = 303

@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)       

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        pin = request.data.get('pin')  
        user = get_object_or_404(CustomUser,phone_number=phone_number)
        print(user)
        if not user.admin:
            return JsonResponse({"detail" :"you are not allowed to login" },status=403)
        if user.disable ==True:
            return JsonResponse({"detail" :"you are not allowed to login" },status=403)
        user = authenticate(request, phone_number=phone_number, password=password)

        print(user)
        if user is not None:
            token =generate_new_token(user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_employee(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        pin = request.data.get('pin')  
        user = get_object_or_404(CustomUser,phone_number=phone_number)
        if not user:
            return JsonResponse({"detail" :"you are not registered" },status=403)
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            token =generate_new_token(user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_token_and_pin(request):
    if request.method == 'POST':
        token_key = request.data.get('token')
        pin = request.data.get('pin')
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.pin == pin:
            new_token =generate_new_token(user)
            return Response({'token': new_token.key}, status=status.HTTP_200_OK)
        else:

            return Response({'error': 'Invalid PIN'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_pin(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')
        new_pin = request.data.get('new_pin')
        otp_entered = request.data.get('otp')
        if not (phone_number and new_pin and otp_entered):
            return JsonResponse({'error': 'Phone number, OTP, and new PIN are required in the request'}, status=400)
  

        user = get_object_or_404(CustomUser, phone_number=phone_number)

      
        otp_instances = OTP.objects.filter(user=user, otp=otp_entered)
        if not otp_instances.exists():
            return JsonResponse({'error': 'Invalid OTP'}, status=400)
        elif otp_instances.count() > 1:

            otp_instances.delete()
            return JsonResponse({'error': 'Multiple OTPs found. Please try again.'}, status=400)

        user.pin = new_pin
        user.save()

        otp_instances.delete()

        return JsonResponse({'message': 'PIN reset successfully'})
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)


        
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_otp(request):
    phone_number = request.data.get('phone_number')
    if not phone_number:
        return JsonResponse({'error': 'Phone number required'}, status=400)

    user = get_object_or_404(CustomUser, phone_number=phone_number)

    # Save user in session for confirm
    request.session['reset_user_id'] = user.id

    # Delete old OTPs
    OTP.objects.filter(user=user).delete()

    otp_code = ''.join(random.choices(string.digits, k=4))
    OTP.objects.create(user=user, otp=otp_code)

    # Send SMS/email here
    msg = f"Your password reset OTP is {otp_code}"
    # send_sms(phone_number, msg)  # Uncomment if you have SMS integration
    print(msg)

    return JsonResponse({'message': 'OTP sent successfully'})



@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    phone_number = request.data.get('phone_number')
    otp_entered = request.data.get('otp')

    if not (phone_number and otp_entered):
        return JsonResponse({'error': 'Phone number and OTP are required in the request'}, status=400)

    user = get_object_or_404(CustomUser, phone_number=phone_number)

    otp_queryset = OTP.objects.filter(user=user).order_by('-created_at')

    try:

        user_otp = otp_queryset.first()
    except OTP.DoesNotExist:
        return JsonResponse({'error': 'No OTP object found for the user'}, status=400)

    if otp_entered == user_otp.otp:
        return JsonResponse({'message': 'OTP verification successful'})
    else:
        return JsonResponse({'error': 'Invalid OTP'}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_confirm(request):
    phone_number = request.data.get('phone_number')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    if not (phone_number and otp and new_password):
        return JsonResponse({'error': 'Phone number, OTP, and new password required'}, status=400)

    user = get_object_or_404(CustomUser, phone_number=phone_number)
    otp_record = OTP.objects.filter(user=user, otp=otp).first()

    if not otp_record:
        return JsonResponse({'error': 'Invalid OTP'}, status=400)

    # Update password
    user.set_password(new_password)
    user.save()

    otp_record.delete()

    return JsonResponse({'message': 'Password reset successfully'})
   

#    ---------------------------- super admin ------------------------------------------


# ----------------- super admin web --------------------------

# UGRADE UDMIN USER TO SUPER USER
@api_view([ 'PUT'])
def upgrade_admin_user(request,pk):    
    user=request.user
    employee = user.employee if user.employee else None
    allow,instance,allow_msg= allow_user(request,CustomUser,instance=False,pk=pk)  # CHANGE model
    if not allow:
        return JsonResponse({"details" : allow_msg} , status=401)
    company,company_msg=get_user_company(user)
    company_id=get_company_id(company)

    user =get_object_or_404(CustomUser,id=pk)
    serializer = UpgradeUserSerializer(user,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=200)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# ADD BRANCH IN WEB
@api_view([ 'PUT'])
def add_branch(request,pk):  
    user=request.user
    employee = user.employee if user.employee else None
    allow,instance,allow_msg= allow_user(request,CustomUser,instance=False,pk=pk)  # CHANGE model
    if not allow:
        return JsonResponse({"details" : allow_msg} , status=401)
    company,company_msg=get_user_company(user)
    company_id=get_company_id(company)

    user =get_object_or_404(CustomUser,id=pk)
    # Extract company data
    company = {
        'name': request.POST.get('company_name'),
        'email': request.POST.get('company_email'),
        'phone': request.POST.get('company_phone'),
        'address': request.POST.get('company_address'),
        
    }

    serializer = BranchCreateSerializer(user,data={**request.POST.dict(),"company" :company})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=200)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET', 'PUT'])
def get_me(request):    
    user=request.user
    employee = user.employee if user.employee else None
    allow,instance,allow_msg= allow_user(request,CustomUser,instance=False,pk=False)  # CHANGE model
    if not allow:
        return JsonResponse({"details" : allow_msg} , status=401)
    company,company_msg=get_user_company(user)
    company_id=get_company_id(company)

    if request.method == 'GET':
        if user.company:
             ser = CompanyAdminProfileSerializer(user, many=False)
        else:
            ser = AdminOwnerSerializer(user, many=False)
        return Response(ser.data)
    elif request.method == 'PUT':
        request_data = request.data.copy()
        request_data.pop('password', None)
        request_data.pop('pin', None)
        ser = UserSerializer(user, data=request_data, partial=True) 
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
    


# web



reset_codes = {}

# DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


def password_reset_request_view(request):
    error = {}
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                error['email'] = "Email not found"
                return render(request, "password_reset_request.html", {"form": form, "error": error})

            # Generate reset code
            reset_code = get_random_string(length=6)

            # Save OTP
            OTP.objects.filter(user=user).delete()
            OTP.objects.create(user=user, otp=reset_code)

            # Save user in session
            request.session['reset_user_id'] = user.id

            # Send email
            send_password_reset_email(email, reset_code)

            return redirect(reverse("password_reset_confirm"))
        else:
            error['email'] = "Enter a valid email"
    else:
        form = PasswordResetRequestForm()

    return render(request, "password_reset_request.html", {"form": form, "error": error})


def password_reset_confirm_view(request):
    error = {"otp": "", "confirm_password": "", "user": ""}
    form = SetPasswordForm(request.POST or None)

    # Get user from session
    user_id = request.session.get("reset_user_id")
    user = CustomUser.objects.filter(id=user_id).first() if user_id else None

    if request.method == "POST":
        if not user:
            error['user'] = "User session expired. Please request password reset again."
            return render(request, "password_reset_confirm.html", {"form": form, "error": error})

        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if new_password != confirm_password:
                error['confirm_password'] = "Passwords do not match"
                return render(request, "password_reset_confirm.html", {"form": form, "error": error})

            code = request.POST.get("code")
            otp = OTP.objects.filter(user=user, otp=code).first()

            if not otp:
                error['otp'] = "Invalid OTP"
                return render(request, "password_reset_confirm.html", {"form": form, "error": error})

            # Update password
            user.set_password(new_password)
            user.save()

            # Delete OTP
            otp.delete()

            # Clear session
            if "reset_user_id" in request.session:
                del request.session["reset_user_id"]

            return redirect("login")

        else:
            return render(request, "password_reset_confirm.html", {"form": form, "error": error})

    return render(request, "password_reset_confirm.html", {"form": form, "error": error})



import logging
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail

logger = logging.getLogger("app")

# ============================================================
#               SEND EMAIL
# ============================================================
def send_password_reset_email(email, reset_code):
    try:
        send_mail(
            "Password Reset",
            f"Your reset code is: {reset_code}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        print("Password reset email sent successfully")
    except Exception as e:
        logger.error(f"Error sending password reset email to {email}: {e}")
        raise e
