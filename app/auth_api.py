
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializer import *
from .utils import *
import string
import random

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
    pin =request.query_params.get('pin',None)
    generated_otp = ''.join(random.choices(string.digits, k=4))
    if pin =="true":
        msg=f"This is your Mobile PIN Reset OTP {generated_otp} vinsupinfotech."  
    elif pin =="false":
        msg=f"This is your password Reset OTP {generated_otp} vinsupinfotech"
    else:
        return JsonResponse({'error': 'Invalid Request'}, status=400)

    if not phone_number:
        return JsonResponse({'error': 'Phone number is required in the request'}, status=400)
    
    user = get_object_or_404(CustomUser, phone_number=phone_number)
    otp_obj = OTP.objects.filter(user=user)
    if otp_obj.count:
        otp_obj.delete()
    otp_instance = OTP.objects.create(user=user, otp=generated_otp)

    is_send = send_sms(phone_number,msg,templateid=False)
    if not is_send:
        return JsonResponse({ 'message': message_server_error},status=message_server_error_status)
    return JsonResponse({ 'message': 'OTP sent successfully'})



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
    new_pin = request.data.get('new_pin')

    new_password = request.data.get('new_password')

    if not (phone_number and otp ):
        return JsonResponse({'error': 'Phone number, OTP, and new PIN are required in the request'}, status=400)

    user = get_object_or_404(CustomUser, phone_number=phone_number)

    # Check if the user has a valid OTP stored
    user_otp = OTP.objects.filter(user=user).last()
    if user_otp is None:
        return JsonResponse({'error': 'No OTP found for the provided phone number'}, status=400)
    
    if(not new_pin and not new_password):
           return JsonResponse({'error': 'Invalid Request'}, status=400)
    print(user_otp,user)
    if otp == user_otp.otp:
        if new_pin:
            user.pin = new_pin
        if new_password :
            user.set_password(new_password)
        user.save()

        user_otp.delete()

        return JsonResponse({'message': 'reset  confirm successfully'})
    else:
        return JsonResponse({'error': 'Invalid OTP'}, status=400)

   