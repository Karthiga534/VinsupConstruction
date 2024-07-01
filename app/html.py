import logging
from .utils import *
from app.auth_ser import *
from .forms import LoginForm
from .models import CustomUser
from rest_framework import status
from .auth_models import OwnerInfo
from django.db.models import Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
logger = logging.getLogger(__name__)


# TEMPLATE_PATH ='superadmin'

# def login_admin(request):
#     if request.method =="POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
         
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']

#             try:
#                 user = CustomUser.objects.get(email=email)
#                 if user.check_password(password):
#                     login(request, user)
#                     if not user.is_staff :
#                         return redirect("login-admin")
#                     return redirect("admin-dashboard")
                   
#                 else:
#                     return render(request,"login.html", {'form': form})
                   
#             except CustomUser.DoesNotExist:
#                 print("User does not exist")
            
#             user =authenticate(request, email=email, password=password)

#         else:
#             print(form.errors)
#     form = LoginForm()
#     return render(request,f"{TEMPLATE_PATH}/login.html", {'form': form})

TEMPLATE_PATH ='superadmin'

def login_admin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            user = None
            try:
                if '@' in identifier:
                    user = CustomUser.objects.get(email=identifier)
                else:
                    user = CustomUser.objects.get(phone_number=identifier)

                if user.check_password(password):
                    login(request, user)
                    if not user.is_staff:
                        return redirect("login-admin")
                    return redirect("admin-dashboard")
                else:
                    return render(request, "login.html", {'form': form, 'error': "Invalid password"})
            except CustomUser.DoesNotExist:
                return render(request, "login.html", {'form': form, 'error': "User does not exist"})
        else:
            return render(request, "login.html", {'form': form, 'errors': form.errors})
    else:
        form = LoginForm()
        return render(request, f"{TEMPLATE_PATH}/login.html", {'form': form})




def logout_admin(request):
    user=request.user
    if user.is_authenticated:
        logout( request)
        form = LoginForm()
        return render(request,f"{TEMPLATE_PATH}/login.html", {'form': form})
    return redirect("/")

from django.db.models import Q
from app.utils import customPagination


def allow_super_user(request):
    user =request.user
    allow_msg ='not allowed'
  
    return True ,allow_msg 

@login_required(login_url='login-admin')
def Index(request):
    allow,allow_msg= allow_super_user(request)  
    if not allow:
        return redirect("login-admin")
    
    customers =CustomUser.objects.filter(is_owner=True,admin=True).order_by('-id')
    # customers =CustomUser.objects.all()
    queryset,pages,search =customPagination(request,CustomUser,customers)
    print(pages)
    context= {'list': queryset,"location":"admin-dashboard","pages" :pages,'search' :search}
    return render(request,f"{TEMPLATE_PATH}/adminuser.html",context)


@login_required(login_url='login-admin')
def super_users(request):
    allow,allow_msg= allow_super_user(request)  
    if not allow:
        return redirect("login-admin")
    
    customers =CustomUser.objects.filter(is_owner=True,admin=False).order_by('-id')
    queryset,pages,search =customPagination(request,CustomUser,customers)
    
    context= {'list': queryset,"location":"super-users","pages" :pages,'search' :search}
    return render(request,f"{TEMPLATE_PATH}/superadminuser.html",context)


import secrets
from .forms import RegistrationForm

def register_user(request):
    allow,allow_msg= allow_super_user(request)  
    if not allow:
        return redirect("login-admin")
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            random_password = secrets.token_urlsafe(12)  # Generates a 12-character random password
            proof_file = form.cleaned_data['proof']
            if proof_file:
                user_proof = CustomUser.proof.field.upload_to + proof_file.name
                with open(user_proof, 'wb+') as destination:
                    for chunk in proof_file.chunks():
                        destination.write(chunk)

            # Create a new user object with the random password
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=random_password,
                name=form.cleaned_data['name'],
                phone_number=form.cleaned_data['phone_number'],
                # address=form.cleaned_data['address'],
                # proof=form.cleaned_data['proof']
                proof=user_proof if proof_file else None ,
                is_owner=True
            )
            if user:
                info =OwnerInfo.objects.create(owner=user,
                        proof=user_proof if proof_file else None ,
                        address=form.cleaned_data['address'],

                                               )

            print(3)
            # form.save()
            return redirect("admin-dashboard")
        else :
            print(form.errors)  
            return redirect("admin-dashboard")
    else:
        form = RegistrationForm()
        return redirect("admin-dashboard")



@login_required(login_url='login-admin')
def remove_user(request,pk):
    allow,allow_msg= allow_super_user(request)  
    if not allow:
        return redirect("login-admin")
    
    customer =get_object_or_404(CustomUser,id=pk)
    customer.delete()
    return redirect("admin-dashboard")



@login_required(login_url='login-admin')
def edit_user(request,pk):
    allow,allow_msg= allow_super_user(request)  
    if not allow:
        return redirect("login-admin")

    customer =get_object_or_404(CustomUser,id=pk)
    form = RegistrationForm(request.POST, request.FILES,instance=customer)
    if form.is_valid():

        form.save()

    return redirect("admin-dashboard")


@api_view(['GET'])
def get_user(request, id):
    allow,allow_msg= allow_super_user(request)  
    if not allow:
        return redirect("login-admin")
    
    try:
        instance = CustomUser.objects.get(id=id)
        ser = AdminOwnerSerializer(instance)
        data = {'data': ser.data}
        return JsonResponse(data, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)


@api_view(['DELETE'])
def delete_user(request, pk):
    allow,allow_msg= allow_super_user(request)  
    if not allow:
        return redirect("login-admin")
    
    try:
        instance = CustomUser.objects.get(id=pk)
        instance.delete()
        return JsonResponse({'message': 'Data deleted successfully'}, status=204)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404)


# @api_view(['PUT'])
# def update_user(request,pk):
#     if request.method == 'PUT':
#         try:
#             instance = CustomUser.objects.get(id=pk)
#             ser = AdminOwnerSerializer(instance, data=request.data)
#             if ser.is_valid():
#                 ser.save()
#                 data = {'data': ser.data}
#                 return JsonResponse(data)
#             else:
#                 return JsonResponse({'error': ser.errors}, status=400)
#         except CustomUser.DoesNotExist:
#             return JsonResponse({'error': 'Data not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
    


# @api_view(['POST'])
# def register_customuser(request):
#     if request.method == 'POST':
#         address=request.POST.get("address",None)
#         proof =request.FILES

#         # company_address=request.POST.get("company_address",None)
#         # company_email=request.POST.get("company_email",None)
#         # company_name=request.POST.get("company_name",None)
#         # company_phone_number=request.POST.get("company_phone_number",None)
#         print(address,proof)
#         request_data =request.data.copy().dict()   
#         if address :
#             request_data["address"] =address
#         if proof:
#             request_data["proof"] =proof
#         ser = AdminOwnerSerializer(data=request_data)
#         if ser.is_valid():
#             ser.save()
#             data = {'data': ser.data}
#             return JsonResponse(data ,status=201)
#         else:
#             return JsonResponse({'error': ser.errors}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
    


@api_view(['POST'])
def register_customuser(request) :
    allow,allow_msg= allow_super_user(request)  
    if not allow:
        return redirect("login-admin")
    

    if request.method == 'POST':
        user_data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'), 
        }
        
        # Extract company data
        company = {
            'name': request.POST.get('company_name'),
            'email': request.POST.get('company_email'),
            'phone': request.POST.get('company_phone'),
            'address': request.POST.get('company_address'),
        }

        # Extract address data
        owner = {
            'address': request.POST.get('address'),
            "proof" :request.FILES.get("proof",None),
            "img" :request.FILES.get("img",None),
        }

        serializer = AdminOwnerSerializer(data={**request.POST.dict(),"owner":owner,"company" :company})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_user(request,pk):
    allow,allow_msg= allow_super_user(request)  
    if not allow:
        return redirect("login-admin")
    
    if request.method == 'PUT':
        try:
            instance = CustomUser.objects.get(id=pk)
            user_data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
        }
        
            # Extract company data
            company = {
                'name': request.POST.get('company_name'),
                'email': request.POST.get('company_email'),
                'phone': request.POST.get('company_phone'),
                'address': request.POST.get('company_address'),
            }

            # Extract address data 
            owner = {
                'address': request.POST.get('address'),
                "proof" :request.FILES.get("proof",None),
                "img" :request.FILES.get("img",None)
            }

            user_data["company"] = company
            user_data ["owner"] =owner
            ser = AdminOwnerUpdateSerializer(instance, data={**request.POST.dict(),"owner":owner,"company" :company} ,partial=True)
            if ser.is_valid():
                ser.save()
                data = {'data': ser.data}
                return JsonResponse(data)
            else:
                return JsonResponse( ser.errors, status=400)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Data not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    






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

    



def test (request):
    return render(request,f"{TEMPLATE_PATH}/userregister.html")


