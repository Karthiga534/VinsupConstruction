from .forms import *
from .models import *
from .serializer import *
# from contextvars import Token
from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from django.http import QueryDict
from django.db import transaction
from django.db.models import Count
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.core.mail import send_mail
from .utils import filter_by_date_range
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.http import HttpResponseBadRequest
from django.contrib.auth.views import LogoutView
from .models import Project, Employee, Contractor
from rest_framework.authtoken.models import Token
from django.utils.crypto import get_random_string
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, JsonResponse
from rest_framework.pagination import PageNumberPagination
from .forms import PasswordResetRequestForm, SetPasswordForm
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from app.decorators import check_user_company,check_valid_user,check_admin
from app.utils import PaginationAndFilter, customPagination,check_user,get_current_month,filter_by_month_range,get_company





paginator = PageNumberPagination()
date_format = "%Y-%m-%d"
clocked_in_message ='already clocked in for this date'

message_server_error = "message sending error"
message_server_error_status = 303

def post_data(request,id):
    request_data = request.data.copy()
    request_data['company'] =id
    return request_data


#---------------------------------------------------------------- Dharshini --------------------------------------------------------------------------

#------------------- Custom User -----------------------

def login_admin(request):
    form = LoginForm()
    errors ={}
    if request.method == "POST":  
        form = LoginForm(request.POST)
        errors ={}
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password'] 

            try:
                user = CustomUser.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)                 
                    return redirect("index")
                else:
                    errors['password'] = 'Invalid Password'
            except CustomUser.DoesNotExist:
                errors['email'] = 'Invalid Email Id'
        print(errors,'errors')
        return render(request, "login.html", {'form': form, 'errors': errors,'cred':{"email":email,"password":password}})
    
    return render(request, "login.html", {'form': form, 'errors': errors})



class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login') 

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return super().dispatch(request, *args, **kwargs)
        else:
            # Handle invalid method (GET, PUT, etc.) with a proper response
            from django.http import HttpResponseNotAllowed
            return HttpResponseNotAllowed(['POST'])

#--------------------- Dashboard Table ---------------------

@login_required(login_url='login')
def index(request):
    company, _ = get_company(request.user)

    queryset = Project.objects.filter(is_disabled=False, company__in=company)
    ongoing = queryset.filter(status__code=1)
    completed = queryset.filter(status__code=0)

    project_count = queryset.count()
    employee_count = Employee.objects.filter(user__disable = False,company__in=company).count()
    contractor_count = Contractor.objects.filter(company__in=company).count()
    quatation_count = Quatation.objects.filter(company__in=company).count()
    projectsubcontract_count = ProjectSubContract.objects.filter(company__in=company).count()
    companylabour_count = CompanyLabours.objects.filter(company__in=company, disable=False).count()
    expense_count = Expense.objects.filter(company__in=company).count()
    ongoing_project_count = ongoing.count()
    completed_project_count = completed.count()

    return render(request, 'index.html', {
        'project_count': project_count,
        'employee_count': employee_count,
        'contractor_count': contractor_count,
        'quatation_count': quatation_count,
        'projectsubcontract_count': projectsubcontract_count,
        'companylabour_count': companylabour_count,
        'expense_count': expense_count,
        'ongoing_project_count': ongoing_project_count,
        'completed_project_count': completed_project_count,
    })

#----------------------- Company Staff Table ----------------------

#--------------> Employee Role <-----------------

@login_required(login_url='login')
def emproles(request):
    user=request.user
    allow,msg= check_user(request,EmpRoles,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)  
    if request.method == 'POST':
        form = EmpRolesForm(request.POST)
        if form.is_valid():
            emproles_instance = form.save(commit=False)  
            emproles_instance.company = request.user.company  
            emproles_instance.save()
            return JsonResponse({"msg":"success"},status=201)
        else:
            return JsonResponse({"msg":"error"},status=400)
    else:
        form = EmpRolesForm()    
    querysets = EmpRoles.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,EmpRoles,querysets)    #change, model
    context= {'queryset': queryset,"location":"emproles","pages" :pages,"search":search ,'form':form,}   #change location name 
    return render(request,'employee/emprole.html',context)  


    if request.method == 'POST':
        form = EmpRolesForm(request.POST)
        if form.is_valid():
            emproles_instance = form.save(commit=False)  
            emproles_instance.company = request.user.company  
            emproles_instance.save()
            return JsonResponse({"msg":"success"},status=201)
        else:
            return JsonResponse({"msg":"error"},status=400)
    else:
        form = EmpRolesForm()

    print("User company:", request.user.company)
    emproles = EmpRoles.objects.filter(company=request.user.company).order_by("-id")
    print("Filtered emproles:", emproles)

    return render(request, 'employee/emprole.html', {'form':form,'emproles':emproles})

# @api_view(['POST'])
# @check_valid_user
# @check_user_company
# @check_admin
# @login_required(login_url='login')
# def add_uom(request):
#     user = request.user
#     allow, msg = check_user(request, Uom, instance=False)    
#     if not allow:
#         return JsonResponse({'details': msg}, status=status.HTTP_403_FORBIDDEN)      

#     request_data = request.data.copy() 
    
#     if user.admin:  
#         request_data['company'] = user.company.id

#     serializer = UomSerializer(data=request_data)  
    
#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def add_emproles(request):
    user = request.user
    allow, msg = check_user(request, EmpRoles, instance=False)    
    if not allow:
        return JsonResponse({'details': msg}, status=status.HTTP_403_FORBIDDEN)  
    request_data=request.POST.copy()
    if user.admin:  
        request_data['company'] = user.company.id
    print("request_data:", request_data)
    ser = EmpRolesSerializer(data=request_data)  
    if ser.is_valid():
        ser.save()
        return JsonResponse(ser.data,status=201)    
    else:
        return JsonResponse(ser.errors,status=400)


# @api_view(['PUT'])
# def update_emproles(request, id):
#     try:
#         instance = EmpRoles.objects.get(id=id)
#     except EmpRoles.DoesNotExist:
#         return Response({'error': 'EmpRoles object does not exist'}, status=404)

#     if request.method == 'PUT':
#         serializer = EmpRolesSerializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({'data': serializer.data}, status=200)
#         else:
#             # return JsonResponse({'name': ['Invalid request method']}, status=400)
#             return JsonResponse(serializer.errors, status=400)
#     else:
#         return JsonResponse({'error': ['Invalid request method']}, status=405)    

@api_view(['PUT'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def update_emproles(request, id):  
    user = request.user
    
    try:
        company = request.company
        if hasattr(company, '__iter__') and not isinstance(company, str):
            company = company[0] if company else None
        
        if not company:
            return JsonResponse({'details': 'Invalid or missing company reference'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance = EmpRoles.objects.get(id=id, company=company)  
    except EmpRoles.DoesNotExist:              
        return JsonResponse({'details': 'Emp Roles object does not exist'}, status=404)
    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
        return JsonResponse({'details': 'Invalid company reference'}, status=status.HTTP_400_BAD_REQUEST)
    
    allow, msg = check_user(request, EmpRoles, instance=instance)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = EmpRolesSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@login_required(login_url='login')
def get_emproles(request, id):
    try:
        print("enter")
        # instance = EmpRoles.objects.filter(companyname=request.user.company)
        instance = EmpRoles.objects.get(id=id)
        ser=EmpRolesSerializer(instance,many=False)
        data = {'data': ser.data}
        return JsonResponse(data,status=200)
    except EmpRoles.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)



@api_view(['PUT'])
@login_required(login_url='login')
def save_emproles(request, id):
    user=request.user
    allow,msg= check_user(request,EmpRoles,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)  
    
    # user =get_company_id(user)
    company,company_msg=get_user_company(user)
    company_id=get_company_id(company)
    try:
        instance = EmpRoles.objects.get(id=id)
    except EmpRoles.DoesNotExist:
        return Response({'error': 'EmpRoles object does not exist'}, status=404)

    if request.method == 'PUT':
        serializer = EmpRolesSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data}, status=200)
        else:
            # return JsonResponse({'name': ['Invalid request method']}, status=400)
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': ['Invalid request method']}, status=405)    



@api_view(['DELETE'])
@login_required(login_url='login')
def delete_emproles(request, id):
    try:
        print("enter")
        instance = EmpRoles.objects.get(id=id)
        instance.delete()
        return JsonResponse({'message': 'Data deleted successfully'}, status=204)
    except EmpRoles.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404)

#--------------------> Employee <-----------------------

    
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def employee(request):
    user = request.user
    allow, msg = check_user(request, Employee, instance=False)
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)
    
    if request.method == 'POST':
        request_data = request.POST.copy().dict()
        if user.admin:
            request_data["company"] = user.company.id

        img = request.FILES.get("img", None)
        aadhaar_card_image = request.FILES.get("aadhaar_card_image", None)
        pan_card_image = request.FILES.get("pan_card_image", None)

        # Associate the files with the request data if they exist
        if img:
            request_data['img'] = img

        if aadhaar_card_image:
            request_data['aadhaar_card_image'] = aadhaar_card_image

        if pan_card_image:
            request_data['pan_card_image'] = pan_card_image

        form = EmployeeSerializer(data=request_data)  
        if form.is_valid():
            form.save()
            return JsonResponse({"msg": "success"}, status=201)
        else:
            return JsonResponse(form.errors, status=400)
    
    else:
        form = EmployeeSerializer()
    
    querysets = Employee.objects.filter(company=request.user.company).order_by("-id")
    queryset, pages, search = customPagination(request, Employee, querysets)
    roles = EmpRoles.objects.filter(company=request.user.company)

    context = {
        'queryset': queryset,
        "location": "employee",
        "pages": pages,
        "search": search,
        "roles": roles,
        'form': form
    }

    return render(request, "employee/employee.html", context)


@api_view(['GET'])
@login_required(login_url='login')
def get_employee(request, id):
    try:
        print("enter")
        instance = Employee.objects.get(id=id)
        ser=EmployeeSerializer(instance,many=False)
        data = {'data': ser.data}
        return JsonResponse(data,status=200)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)    
   


@api_view(['PUT'])
@login_required(login_url='login')
def save_employee(request, id):
    try:
        instance = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee object does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    allow, msg = check_user(request, Employee, instance=instance)
    
    if not allow:
        return Response({"error": msg}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = EmployeeSerializer(instance, data=request.data, partial=True)
    
    if serializer.is_valid():
        # Update only the fields that are provided in request data
        request_data = serializer.validated_data
        
        # Handle special fields like company assignment if user is admin
        if user.admin:
            company_instance = user.company
            request_data['company'] = company_instance
        
        # Handle file uploads separately
        img = request.FILES.get("img", None)
        aadhaar_card_image = request.FILES.get("aadhaar_card_image", None)
        pan_card_image = request.FILES.get("pan_card_image", None)

        if img:
            request_data['img'] = img
        if aadhaar_card_image:
            request_data['aadhaar_card_image'] = aadhaar_card_image
        if pan_card_image:
            request_data['pan_card_image'] = pan_card_image

        # Check if mobile number is provided and update if different
        if 'mobile' in request_data and request_data['mobile'] != instance.mobile:
            # Check if the new mobile number already exists in other records
            if Employee.objects.filter(~Q(id=id), mobile=request_data['mobile']).exists():
                return Response({"mobile": ["This mobile number is already in use."]}, status=status.HTTP_400_BAD_REQUEST)

        # Update the instance with the modified data
        serializer.update(instance, request_data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@login_required(login_url='login')
def delete_employee(request, id):
    try:
        print("enter")
        instance = Employee.objects.get(id=id)
        user = instance.user
        if user:
            user.disable = False if user.disable else True
            user.save()
        # instance.delete()
        return JsonResponse( {'details': [user.disable]},status=200)
        # return JsonResponse({'message': 'Disabled successfully'}, status=204)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404)
    


@api_view(['DELETE'])
@login_required(login_url='login')
def enable_employee(request, id):
    try:
        print("enter")
        instance = Employee.objects.get(id=id)
        user =instance.user
        if user:
            user.disable = False
            user.save()
        # instance.delete()
        return JsonResponse( {'details': [user.disable]},status=200)
        return JsonResponse({'message': 'enabled successfully'}, status=204)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404)
   
#------------------------ UOM Table --------------------------

# @login_required(login_url='login')
# def uom(request):
#     if request.method == 'POST':
#         form = UomForm(request.POST)
#         if form.is_valid():
#             uom_instance = form.save(commit=False)  
#             uom_instance.company = request.user.company  
#             uom_instance.save()  
#             return JsonResponse({"msg":"success"},status=201)
#             # return redirect('uom')  
#     else:
#         form = UomForm()
                   
#     print("User company:", request.user.company)  
#     uom = Uom.objects.filter(company=request.user.company).order_by("-id")
#     print("Filtered Uom:", uom) 
#     return render(request, 'library/uom.html', {'form': form, 'uom': uom})

# @api_view(['GET'])
# def get_data(request, id):
#     try:
#         print("enter")
#         # instance = Uom.objects.filter(company=request.user.company)
#         instance = Uom.objects.get(id=id)
#         ser=UomSerializer(instance,many=False)
#         data = {'data': ser.data} 
#         return JsonResponse(data,status=200)
#     except Uom.DoesNotExist:
#         return JsonResponse({'error': 'Object not found'}, status=404)
    
# @api_view(['PUT'])
# def save_data(request, id):
#     try:
#         instance = Uom.objects.get(id=id)
#     except Uom.DoesNotExist:
#         return Response({'error': 'Uom object does not exist'}, status=404)

#     if request.method == 'PUT':
#         serializer = UomSerializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({'data': serializer.data}, status=200)
#         else:
#             # return JsonResponse({'name': ['Invalid request method']}, status=400)
#             return JsonResponse(serializer.errors, status=400)
#     else:
#         return JsonResponse({'error': ['Invalid request method']}, status=405)

# @api_view(['DELETE'])
# def delete_uom(request, id):
#     try:
#         print("enter")
#         instance = Uom.objects.get(id=id)
#         instance.delete()
#         return JsonResponse({'message': 'Data deleted successfully'}, status=204)
#     except Uom.DoesNotExist:
#         return JsonResponse({'error': 'Data not found'}, status=404)    

# def procategory(request, category_id=None):
#     if category_id:
#         category = get_object_or_404(ProjectCategory, pk=category_id)
#     else:
#         category = None

#     if request.method == 'POST':
#         form = ProjectCategoryForm(request.POST, instance=category)
#         if form.is_valid():
#             form.save()
#             return redirect('procategory')
#     else:
#         form = ProjectCategoryForm(instance=category)
    
#     categories = ProjectCategory.objects.all()  
    
#     return render(request, 'procategory.html', {'form': form, 'categories': categories})

#-------------------------------------------------------------------- End Azar --------------------------------------------------------------------------------

#-------------------------------------------Contractor category Table ------------------------------------------------------

# contract category
@login_required(login_url='login')
def contract_category(request):  #change name 
    user=request.user
    allow,msg= check_user(request,Contractcategory,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)      
    querysets = Contractcategory.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,Contractcategory,querysets)    #change, model
    context= {'queryset': queryset,"location":"contractcategory","pages" :pages,"search":search}   #change location name 
    return render(request,"contractor/contractcategory.html",context)    #change template name

@api_view(['POST'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def add_contract_category (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,Contractcategory,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data=request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id

    serializer = ContractcategorySerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       

@api_view(['PUT'])
@login_required(login_url='login')
@check_valid_user
@check_user_company
@check_admin
def update_contract_category(request, pk):  # CHANGE name
    user = request.user
    
    try:
        instance = Contractcategory.objects.get(id=pk)  # CHANGE model
    except Contractcategory.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Contractcategory object does not exist'}, status=404)
    
    allow, msg = check_user(request, Contractcategory, instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details': [msg]}, status=401)
    
    # Create a mutable copy of request.data
    request_data = request.data.copy()
    
    if user.admin:
        request_data['company'] = user.company.id

    serializer = ContractcategorySerializer(instance, data=request_data, partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=400)

    

@api_view(['DELETE'])
@login_required(login_url='login')
def delete_contract_category(request,pk):
    user=request.user
    try:
        instance = Contractcategory.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,Contractcategory,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except Contractcategory.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    
#------------------------------------------------------------------contractor----------------------------------------------------
  
# contract category
@login_required(login_url='login')
def contractor(request):  #change name 
    user=request.user
    allow,msg= check_user(request,Contractor,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)      
    querysets = Contractor.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,Contractor,querysets)    #change, model
    category=Contractcategory.objects.filter(company=request.user.company)
    contractor_count = querysets.count()
    uom =Uom.objects.filter(company=user.company)
    context= {'queryset': queryset,"location":"contractor","pages" :pages ,"categories":category,"search":search, 
              "contractor_count": contractor_count,'uom':uom}   #change location name 
    return render(request,"contractor/contractor.html",context)    #change template name
 
@api_view(['POST'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def add_contractor (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,Contractor,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data=request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id

    serializer = ContractorSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(['PUT'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def update_contractor(request, pk):
    user = request.user
    
    try:
        company = request.company
        if hasattr(company, '__iter__') and not isinstance(company, str):
            company = company[0] if company else None
        
        if not company:
            return JsonResponse({'details': 'Invalid or missing company reference'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance = Contractor.objects.get(id=pk, company=company)  
    except Contractor.DoesNotExist:              
        return JsonResponse({'details': 'Contract Category object does not exist'}, status=404)
    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
        return JsonResponse({'details': 'Invalid company reference'}, status=status.HTTP_400_BAD_REQUEST)
    
    allow, msg = check_user(request, Contractor, instance=instance)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ContractorSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
@login_required(login_url='login')
def delete_contractor(request,pk):
    user=request.user
    try:
        instance = Contractor.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,Contractor,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except Contractor.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)

@login_required(login_url='login')
def machinary_charges(request):   #change name 
    user = request.user
    allow, msg = check_user(request, CompanyMachinaryCharges, instance=False)   # CHANGE model
    if not allow:
         context = {"unauthorized": msg}
         return render(request, "login.html", context)
    querysets = CompanyMachinaryCharges.objects.filter(company=request.user.company).order_by("-id")  #change query
    payment_schedules = PaymentSchedule.objects.all()#order_by("-id") 
    queryset, pages, search = customPagination(request, CompanyMachinaryCharges, querysets)   #change, model
    context = {
        'queryset': queryset,
        "location": "machinary_charges",
        "payment_schedules": payment_schedules,
        "pages": pages,
        "search": search,
    }
    return render(request, "library/machinarycharges.html", context)    #change template name

@api_view(['POST'])
@check_valid_user
@check_user_company
@login_required(login_url='login')
def add_machinary_charges (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,CompanyMachinaryCharges,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data=request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id

    serializer = CompanyMachinaryChargesSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PUT'])
@check_valid_user
@check_user_company
@login_required(login_url='login')
def update_machinary_charges(request, pk):  # CHANGE name
    user=request.user

    try:
        instance = CompanyMachinaryCharges.objects.get(id=pk)  # CHANGE model
    except CompanyMachinaryCharges.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Category object does not exist'}, status=404)
    
    if user.company != instance.company:
        return JsonResponse({'details': 'Unauthorized to update this object'}, status=401)
    
    allow,msg= check_user(request,CompanyMachinaryCharges,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = CompanyMachinaryChargesSerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@login_required(login_url='login')
def delete_machinary_charges(request,pk):
    user=request.user
    try:
        instance = CompanyMachinaryCharges.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,CompanyMachinaryCharges,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except CompanyMachinaryCharges.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)    

#-----------------------------------------labour roles AND SALARY  ---------------------------------
@login_required(login_url='login')
def labour_roles_and_salary(request):
    user = request.user
    allow, msg = check_user(request, LabourRolesAndSalary, instance=False)
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)
    
    querysets = LabourRolesAndSalary.objects.filter(company=request.user.company).order_by("-id")
    queryset, pages, search = customPagination(request, LabourRolesAndSalary, querysets)
    payment_schedules = PaymentSchedule.objects.all()
    context = {'queryset': queryset, "location": "labour_roles_and_salary","payment_schedules": payment_schedules, "pages": pages, "search": search}
    return render(request, "library/labourrolesandsalary.html", context)



@api_view(['POST'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def add_labour_roles_and_salary(request):
    user = request.user
    allow, msg = check_user(request, LabourRolesAndSalary, instance=False)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data = request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id

    serializer = LabourRolesAndSalarySerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def update_labour_roles_and_salary(request, pk):
    user = request.user
    
    try:
        company = request.company
        if hasattr(company, '__iter__') and not isinstance(company, str):
            company = company[0] if company else None
        
        if not company:
            return JsonResponse({'details': 'Invalid or missing company reference'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance = LabourRolesAndSalary.objects.get(id=pk, company=company)  
    except MaterialLibrary.DoesNotExist:              
        return JsonResponse({'details': 'Labour Roles And Salary object does not exist'}, status=404)
    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
        return JsonResponse({'details': 'Invalid company reference'}, status=status.HTTP_400_BAD_REQUEST)
    
    allow, msg = check_user(request, LabourRolesAndSalary, instance=instance)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = LabourRolesAndSalarySerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@login_required(login_url='login')
def delete_labour_roles_and_salary(request, pk):
    user = request.user
    try:
        instance = LabourRolesAndSalary.objects.get(id=pk)
        allow, msg = check_user(request, LabourRolesAndSalary, instance=instance)
        if not allow:
            return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse({'details': ['success']}, status=status.HTTP_204_NO_CONTENT)
    except LabourRolesAndSalary.DoesNotExist:
        return JsonResponse({'details': ['Item does not exist']}, status=status.HTTP_404_NOT_FOUND)

#-----------------------------------Labours--------------------------------------------------

@login_required(login_url='login')
def labours(request):   #change name 
    user = request.user
    allow, msg = check_user(request, CompanyLabours, instance=False)   # CHANGE model
    if not allow:
         context = {"unauthorized": msg}
         return render(request, "login.html", context)
    querysets = CompanyLabours.objects.filter(company=request.user.company).order_by("-id")  #change query
    roles = LabourRolesAndSalary.objects.filter(company=request.user.company).order_by("-id") 
    payment_schedules = PaymentSchedule.objects.all()
    queryset, pages, search = customPagination(request, CompanyLabours, querysets)   #change, model
    context = {
        'queryset': queryset,
        "location": "labours",
        "roles":roles,
        "payment_schedules":payment_schedules,
        "pages": pages,
        "search": search,
    }
    return render(request,"library/labours.html", context)    #change template name



@api_view(['POST'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def add_labours (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,CompanyLabours,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data=request.POST.copy().dict()
    images=request.FILES.get("image",None)
    if images:
        request_data['image'] = images
    if user.admin:
        request_data['company'] = user.company.id

    
    serializer = CompanyLaboursSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


@api_view(['PUT'])
@login_required(login_url='login')
@check_valid_user
@check_user_company
@check_admin
def update_labours(request, pk):  # CHANGE name
    user = request.user

    try:
        instance = CompanyLabours.objects.get(id=pk)  # CHANGE model
    except CompanyLabours.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Category object does not exist'}, status=404)
    
    allow, msg = check_user(request, CompanyLabours, instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details': [msg]}, status=401)
    
    # Create a mutable copy of the request data
    data = request.data.copy()
    
    if user.admin:
        data['company'] = user.company.id

    serializer = CompanyLaboursSerializer(instance, data=data, partial=True, context={'request': request})  # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=400)


@api_view(['DELETE'])
@login_required(login_url='login')
def delete_labours(request,pk):
    user=request.user
    try:
        instance = CompanyLabours.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,CompanyLabours,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.disable = False if instance.disable else True
        instance.save()
        # instance.delete()
        return JsonResponse( {'details': [instance.disable]},status=200)
    except CompanyLabours.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)

#-------------------------------------------- Expense -----------------------------

@login_required(login_url='login')
def expense(request):  #change name 
    user=request.user
    allow,msg= check_user(request,Expense,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
      
    querysets = Expense.objects.filter(company=request.user.company).order_by("-id") 
    employee = Employee.objects.filter(company=request.user.company,user__disable = False).order_by("-id") 
    site_location =Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,Expense,querysets)    #change, model
    context= {'queryset': queryset,
              "location":"expense",
              "pages" :pages,
              "employees":employee,
              "site_locations": site_location,
              "search":search,
              }   #change location name 
    return render(request,"expense/expense.html",context)    #change template name

@api_view(['POST'])
@check_valid_user
@check_user_company
# @check_admin
@login_required(login_url='login')
def add_expense (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,Expense,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data=request.POST.copy().dict()
    attachments = request.FILES.get("attachment",None) 

    if user:
        request_data['company'] = user.company.id

    if attachments: 
         request_data['attachment'] = attachments

    serializer = ExpenseSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@check_valid_user
@check_user_company
@login_required(login_url='login')
def update_expense(request, pk):  # CHANGE name
    user=request.user

    try:
        instance = Expense.objects.get(id=pk)  # CHANGE model
    except Expense.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)

    allow,msg= check_user(request,Expense,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ExpenseSerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@login_required(login_url='login')
def delete_expense(request,pk):
    user=request.user
    try:
        instance = Expense.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,Expense,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except Expense.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    
def expense_list(request):
    user = request.user
    allow, msg = check_user(request, Expense, instance=False)   # CHANGE model
    if not allow:
         context = {"unauthorized": msg}
         return render(request, "login.html", context)
    querysets = Expense.objects.filter(company=request.user.company).order_by("-id")  #change query
    project=  Project.objects.filter(company=request.user.company,is_disabled=False).order_by("-id")
    employee =Employee.objects.filter(company=request.user.company,user__disable = False).order_by("-id") 
    queryset, pages, search = customPagination(request, Expense, querysets)   #change, model
    context = {
        'queryset': queryset,
        "location": "expenselist",
        "site_locations":project,
        "pages": pages,
        "search": search,
        "employee" : employee
    }
    return render(request,"expense/expenselist.html", context)


@api_view(['GET'])
def expenselist(request, pk):
    user = request.user
    allow, msg = check_user(request, Expense, instance=False)   # CHANGE model
    if not allow:
         context = {"unauthorized": msg}
         return render(request, "login.html", context)

    querysets = Expense.objects.filter(company=request.user.company).order_by("-id")
    if pk !=int(0) :
        querysets = querysets.filter(site_location__id=pk)
    # # Date Filtering
    # start_date = request.GET.get('start_date')
    # end_date = request.GET.get('end_date')
    # if start_date and end_date:
    #     querysets = querysets.filter(date__range=[start_date, end_date])
    return PaginationAndFilter(querysets, request, ExpenseSerializer,"date")



def invoice(request):
    return render(request, 'invoice.html',{})

def payment(request):
    return render(request, 'payment.html',{})

def permission(request):
    return render(request, 'master/permission.html',{})

def profit(request):
    return render(request, 'profit.html')

def projectlist(request):
    return render(request, 'projectlist.html',{})
# --------------------------------------------------------------------------------------------------------

@login_required(login_url='login')
def labour_salary(request):
    user=request.user
    allow,msg= check_user(request,CompanyLabours,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
      
    querysets = CompanyLabours.objects.filter(company=request.user.company, disable=False).order_by("-id") 
    employees = CompanyLabours.objects.filter(company=request.user.company, disable=False).order_by("-id") 
    paymode=PaymentMethod.objects.all()
    # site_location =Project.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,CompanyLabours,querysets)    #change, model
    context= {'queryset': queryset,
              "location":"labour-salary",
              "pages" :pages,
              "employees":employees,
              "paymode" :paymode ,
            #   "site_locations": site_location,
              "search":search,
              }   #change location name 
    return render(request, 'salary/laboursalary.html',context)



@api_view(['PUT'])
@login_required(login_url='login')
def make_labour_salary(request,pk):

    labour =get_object_or_404(CompanyLabours,id=pk)
    request_data = request.data.copy()
    request_data ['labour'] = pk

    ser=LabourSalaryReceiptHistorySerializer(data=request_data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors,status=400)


@api_view(['PUT'])
@login_required(login_url='login')
def make_labour_payment(request,pk):  #change name 
    user=request.user
    try:
        instance = SalaryReceipt.objects.get(id=pk)  # CHANGE model
    except SalaryReceipt.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'SalaryReceipt object does not exist'}, status=404)
    

    allow,msg= check_user(request,SalaryReceipt,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data = request.data.copy()
    request_data["receipt"] = pk

    serializer = SalaryReceiptHistorySerializer( data=request_data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        ser =LabourSalaryReceiptHistorySerializer(instance,many=False)
        return JsonResponse( ser.data, status=201)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# -------------------------------------------------------------------------------


@login_required(login_url='login')
def employee_salary(request):
    user=request.user
    allow,msg= check_user(request,Employee,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
      
    querysets = Employee.objects.filter(company=request.user.company,user__disable = False).order_by("-id") 
    employee = Employee.objects.filter(company=request.user.company,user__disable = False).order_by("-id") 
    paymode=PaymentMethod.objects.all()
    # site_location =Project.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,Employee,querysets)    #change, model
    context= {'queryset': queryset,
              "location":"salaryreport",
              "pages" :pages,
              "employees":employee,
              "paymode" :paymode ,
            #   "site_locations": site_location,
              "search":search,
              }   #change location name 
    return render(request, 'salary/employeesalary.html',context)


@api_view(['PUT'])
@login_required(login_url='login')
def employee_labour_salary(request,pk):

    labour =get_object_or_404(Employee,id=pk)
    request_data = request.data.copy()
    request_data ['employee'] = pk

    ser=EmployeeSalaryReceiptHistorySerializer(data=request_data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors,status=400)

def signin(request):
    return render(request, 'signin.html',{})

# def viewstock(request):
#     return render(request, 'viewstock.html')

# #------------------------------------------------------------------------------------ City Table -------------------------------------------------------------------------

# @login_required(login_url='login')
# def city(request):
#     city = City.objects.all() 
#     districts = District.objects.all() 
#     return render(request, 'city.html', {'city': city, 'districts': districts})

# def addcity(request): 
#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('city')
#     else:
#         form = CityForm()  

#     districts = District.objects.all()

#     return render(request, 'city.html', {'form': form, 'districts': districts})

# def updatecity(request, id):
#     if request.method == 'POST':
#         city_id = id  
#         district_name = request.POST.get('district_name')
#         city_name = request.POST.get('city_name')  
#         description = request.POST.get('description')

#         city = City.objects.get(pk=city_id)
        
#         # Update the district name
#         city.district.name = district_name

#         # Check if city_name is not empty before updating
#         if city_name:
#             city.name = city_name
        
#         city.description = description
#         city.save()

#         return redirect('city')
    
#     return render(request, 'city.html', {})

# def deletecity(request,id):
#     city=City.objects.filter(id=id)
#     city.delete()

#     context={
#         'city':city,
#     }
#     return redirect('city')

#     return render(request, 'country.html',{})

# #------------------------------------------------------------------------------------ Country -------------------------------------------------------------------------

# @login_required(login_url='login')
# def country(request):
#     country=Country.objects.all()
#     context={
#         'country':country,
#     }
#     return render(request, 'country.html',context)

# def addcountry(request):
#     if request.method == 'POST':
#         form = CountryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('country')
#     else:
#         form = CountryForm()  

#     return render(request, 'country.html', {'form': form})

# def updatecountry(request,id):
#     if request.method == 'POST':
#         name=request.POST.get('name')
#         description=request.POST.get('description')

#         country=Country(
#             id=id,
#             name=name,
#             description=description,
#         )

#         country.save()

#         return redirect('country')
    
#     return render(request, 'country.html',{})

# def deletecountry(request,id):
#     country=Country.objects.filter(id=id)
#     country.delete()

#     context={
#         'country':country,
#     }
#     return redirect('country')

#     return render(request, 'country.html',{})

# #---------------------------------------------------------------------------------District Table -------------------------------------------------------------------------

# @login_required(login_url='login')
# def district(request):
#     districts=District.objects.all()
#     context={
#         'districts':districts,
#     }
#     return render(request, 'district.html',context)

# def adddistrict(request):
#     if request.method == 'POST':
#         form = DistrictForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('district')
#     else:
#         form = DistrictForm()  

#     return render(request, 'district.html', {'form': form})

# def updatedistrict(request,id):
#     if request.method == 'POST':
#         name=request.POST.get('name')
#         description=request.POST.get('description')

#         districts=District(
#             id=id,
#             name=name,
#             description=description,
#         )

#         districts.save()

#         return redirect('district')
    
#     return render(request, 'district.html',{})

# def deletedistrict(request,id):
#     districts=District.objects.filter(id=id)
#     districts.delete()

#     context={
#         'districts':districts,
#     }
#     return redirect('district')

#     return render(request, 'district.html',{})

# #---------------------------------------------------------------------------------- Role Table -------------------------------------------------------------------------

# @login_required(login_url='login')
# def roles(request):
#     roles=Roles.objects.all()
#     context={
#         'roles':roles,
#     }
#     return render(request, 'roles.html',context)

# def addroles(request):
#     if request.method == 'POST':
#         form = RolesForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('roles')
#     else:
#         form = RolesForm()  

#     return render(request, 'roles.html', {'form': form})

# def updateroles(request,id):
#     if request.method == 'POST':
#         name=request.POST.get('name')
#         description=request.POST.get('description')

#         roles=Roles(
#             id=id,
#             name=name,
#             description=description,
#         )

#         roles.save()

#         return redirect('roles')
    
#     return render(request, 'roles.html',{})

# def deleteroles(request,id):
#     roles=Roles.objects.filter(id=id)
#     roles.delete()

#     context={
#         'roles':roles,
#     }
#     return redirect('roles')

#     return render(request, 'roles.html',{})







# from datetime import date
# @login_required(login_url='login')
# def contractor_payment_management(request):

#     user=request.user
#     allow,msg= check_user(request,ProjectSubContract,instance=False)  # CHANGE model
#     if not allow:
#          context ={"unauthorized":msg}
#          return render(request,"login.html",context)      
#     contractors = ProjectSubContract.objects.filter(company=request.user.company).order_by("-id")   #change query
    

#     current_date = date.today()

#     contractors = ProjectSubContract.objects.all()
#     querysets = []

#     for contractor in contractors:
#         start_date = None

#         total_wages =None

#         # Check if the contractor has an invoice
#         invoice = ContractorInvoice.objects.filter(contract=contractor).first()
#         if invoice:
#             start_date = invoice.to_date
#         else:
#             start_date = contractor.start_date

#         last_attendance = ProjectSubContractLabourAttendence.objects.filter(contract=contractor).order_by('-date').first()

#         if last_attendance:
#                 end_date = last_attendance.date
#         else:
#                 end_date = current_date

     

#         if start_date:

#             labour_wages = contractor.projectsubcontractlabourwages

#             if contractor.get_labour_attendence :
#                 total_wages = (
#                     contractor.get_labour_attendence.filter(date__range=[start_date, end_date]).aggregate(
#                         maistry=Sum('maistry') * labour_wages.maistry ,
#                         maison_cooli=Sum('maison_cooli')  * labour_wages.maison_cooli,
#                         male_skilled=Sum('male_skilled') * labour_wages.male_skilled,
#                         male_unskilled=Sum('male_unskilled') * labour_wages.male_unskilled,
#                         female_skilled=Sum('female_skilled') * labour_wages.female_skilled,
#                         female_unskilled=Sum('female_unskilled') * labour_wages.female_unskilled,

#                         maistry_ot=Sum('maistry_ot') * (labour_wages.maistry / 8),
#                         maison_cooli_ot=Sum('maison_cooli_ot') * (labour_wages.maison_cooli /8 ),
#                         male_skilled_ot=Sum('male_skilled_ot') * (labour_wages.male_skilled / 8) ,
#                         male_unskilled_ot=Sum('male_unskilled_ot') * (labour_wages.male_unskilled / 8),
#                         female_skilled_ot=Sum('female_skilled_ot') * (labour_wages.female_skilled / 8 ),
#                         female_unskilled_ot=Sum('female_unskilled_ot') *( labour_wages.female_unskilled /8 )
#                     )
#                 )

#                 # total_wages = sum(total_wages.values())
              


#         query = {
#                 "contractor_id": contractor.id,
#                 "contractor_name": contractor.display,
#                 # "start_date" :start_date ,
#                 #  "end_date" :end_date,
#                 "days" : (end_date -start_date).days,

#                 "project_name" :contractor.project.proj_name,

#                  "total_wages" :total_wages if total_wages else contractor.total_wages ,
#                  "total_amount":contractor.get_contract_amount,

#                   "total_service_amount":contractor.total_service_amount,
#                    "get_paid_amount":contractor.get_paid_amount, 
#                    "get_pending_amount":contractor.get_pending_amount,

#                    "get_contract_invoice":contractor.get_contract_invoice,

               
#             }

#         print(query)
#         querysets.append(query)

    
#     queryset,pages,search =customPagination(request,ProjectSubContract,querysets)    #change, model
#     contractors=Contractor.objects.filter(company=request.user.company)
#     paymode =PaymentMethod.objects.all()
#     context= {'queryset': queryset,"pending":"contractor","pages" :pages ,"contractors":contractors,"search" :search,"paymode" :paymode}   #change location name 
#     return render(request,"salary/contractorpayment.html",context) 


from datetime import date

@login_required(login_url='login')
def contractor_payment_management(request):
    user = request.user
    allow, msg = check_user(request, ProjectSubContract, instance=False)  # Ensure correct permissions
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)

    contractors = ProjectSubContract.objects.filter(company=request.user.company).order_by("-id")

    current_date = date.today()
    querysets = []

    for contractor in contractors:
        start_date = None
        total_wages = None

        # Get the invoice date or fallback to contract start date
        invoice = ContractorInvoice.objects.filter(contract=contractor).first()
        start_date = invoice.to_date if invoice else contractor.start_date

        last_attendance = ProjectSubContractLabourAttendence.objects.filter(contract=contractor).order_by('-date').first()
        end_date = last_attendance.date if last_attendance else current_date

        # Ensure start_date and end_date are not None before calculating days
        if start_date and end_date:
            days = (end_date - start_date).days
        else:
            # Handle missing dates, set to 0 or some other default value
            days = 0

        if start_date:
            labour_wages = contractor.projectsubcontractlabourwages
            if contractor.get_labour_attendence:
                total_wages = (
                    contractor.get_labour_attendence.filter(date__range=[start_date, end_date]).aggregate(
                        maistry=Sum('maistry') * labour_wages.maistry,
                        maison_cooli=Sum('maison_cooli') * labour_wages.maison_cooli,
                        male_skilled=Sum('male_skilled') * labour_wages.male_skilled,
                        male_unskilled=Sum('male_unskilled') * labour_wages.male_unskilled,
                        female_skilled=Sum('female_skilled') * labour_wages.female_skilled,
                        female_unskilled=Sum('female_unskilled') * labour_wages.female_unskilled,
                        maistry_ot=Sum('maistry_ot') * (labour_wages.maistry / 8),
                        maison_cooli_ot=Sum('maison_cooli_ot') * (labour_wages.maison_cooli / 8),
                        male_skilled_ot=Sum('male_skilled_ot') * (labour_wages.male_skilled / 8),
                        male_unskilled_ot=Sum('male_unskilled_ot') * (labour_wages.male_unskilled / 8),
                        female_skilled_ot=Sum('female_skilled_ot') * (labour_wages.female_skilled / 8),
                        female_unskilled_ot=Sum('female_unskilled_ot') * (labour_wages.female_unskilled / 8)
                    )
                )

        query = {
            "contractor_id": contractor.id,
            "contractor_name": contractor.display,
            "days": days,
            "project_name": contractor.project.proj_name,
            "total_wages": total_wages if total_wages else contractor.total_wages,
            "total_amount": contractor.get_contract_amount,
            "total_service_amount": contractor.total_service_amount,
            "get_paid_amount": contractor.get_paid_amount,
            "get_pending_amount": contractor.get_pending_amount,
            "get_contract_invoice": contractor.get_contract_invoice,
        }

        print(query)
        querysets.append(query)

    queryset, pages, search = customPagination(request, ProjectSubContract, querysets)
    contractors = Contractor.objects.filter(company=request.user.company)
    paymode = PaymentMethod.objects.all()
    context = {'queryset': queryset, "pending": "contractor", "pages": pages, "contractors": contractors, "search": search, "paymode": paymode}
    return render(request, "salary/contractorpayment.html", context)




from django.db.models import Q
from .utils import PaginationAndFilter
@api_view(['GET'])
@login_required(login_url='login')
def contractor_payment(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,ProjectSubContract,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
 
    contractors = ProjectSubContract.objects.filter(company=request.user.company).order_by("-id")   #change query
    
    # current_date = date.today()

    # contractors = ProjectSubContract.objects.all()
    querysets = contractors
    pk= int(pk)
    if pk !=0:   
        querysets =querysets.filter(contractor__id =pk)

    # for contractor in contractors:
    #     start_date = None

    #     total_wages =None

    #     # Check if the contractor has an invoice
    #     invoice = ContractorInvoice.objects.filter(contract=contractor).first()
    #     if invoice:
    #         start_date = invoice.to_date
    #     else:
    #         start_date = contractor.start_date

    #     last_attendance = ProjectSubContractLabourAttendence.objects.filter(contract=contractor).order_by('-date').first()
    #     if last_attendance:
    #             end_date = last_attendance.date
    #     else:
    #             end_date = current_date


    #     p= contractor.get_labour_attendence.filter(date__range=[start_date, end_date])

    #     print(p,"kkkkkkkkkkkkkkkk")

    #     if start_date:

    #         labour_wages = contractor.projectsubcontractlabourwages

    #         if contractor.get_labour_attendence :
    #             total_wages = (
    #                 contractor.get_labour_attendence.filter(date__range=[start_date, end_date]).aggregate(
    #                     maistry=Sum('maistry') * labour_wages.maistry ,
    #                     maison_cooli=Sum('maison_cooli')  * labour_wages.maison_cooli,
    #                     male_skilled=Sum('male_skilled') * labour_wages.male_skilled,
    #                     male_unskilled=Sum('male_unskilled') * labour_wages.male_unskilled,
    #                     female_skilled=Sum('female_skilled') * labour_wages.female_skilled,
    #                     female_unskilled=Sum('female_unskilled') * labour_wages.female_unskilled,

    #                     maistry_ot=Sum('maistry_ot') * (labour_wages.maistry / 8),
    #                     maison_cooli_ot=Sum('maison_cooli_ot') * (labour_wages.maison_cooli /8 ),
    #                     male_skilled_ot=Sum('male_skilled_ot') * (labour_wages.male_skilled / 8) ,
    #                     male_unskilled_ot=Sum('male_unskilled_ot') * (labour_wages.male_unskilled / 8),
    #                     female_skilled_ot=Sum('female_skilled_ot') * (labour_wages.female_skilled / 8 ),
    #                     female_unskilled_ot=Sum('female_unskilled_ot') *( labour_wages.female_unskilled /8 )
    #                 )
    #             )

    #             total_wages = sum(total_wages.values())
              


    #     query = {
    #             "contractor_id": contractor.id,
    #             "contractor_name": contractor.display,
    #             # "start_date" :start_date ,
    #             #  "end_date" :end_date,
    #             "days" : (end_date -start_date).days,

    #             "project_name" :contractor.project.proj_name,

    #              "total_wages" :total_wages if total_wages else contractor.total_wages ,
    #              "total_amount":contractor.get_contract_amount,

    #               "total_service_amount":contractor.total_service_amount,
    #                "get_paid_amount":contractor.get_paid_amount, 
    #                "get_pending_amount":contractor.get_pending_amount,

    #                "get_contract_invoice":contractor.get_contract_invoice,
    #                 "created_at":contractor.created_at,
               
    #         }

    #     print(query)
    #     querysets.append(query)
      
    # querysets=querysets.none()
    return PaginationAndFilter(querysets, request, ProjectSubContractListSerializer,date_field ="created_at")


@api_view(['GET'])
@login_required(login_url='login')
def contractor_payment_date(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,ProjectSubContract,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
 
    try:
        pk= int(pk)
        instance = ProjectSubContract.objects.get(id=pk)  # CHANGE model
    except ProjectSubContract.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Contractor object does not exist'}, status=404)
    


    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # querysets =filter_by_date_range(querysets,start_date,end_date,date_field ='created_at')
    # to be worked for date in labour attendence
    return PaginationAndFilter(instance, request, ProjectSubContractListSerializer,date_field ="created_at")


@api_view(['PUT'])
@login_required(login_url='login')
def make_contract_payment(request,pk):  #change name 
    user=request.user
    try:
        instance = ProjectSubContract.objects.get(id=pk)  # CHANGE model
    except ProjectSubContract.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Contractor object does not exist'}, status=404)
    

    allow,msg= check_user(request,ProjectSubContract,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data = request.data.copy()
    request_data["contract"] =pk

    serializer = ContractorInvoiceSerializer( data=request_data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=201)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@login_required(login_url='login')
def make_invoice_payment(request,pk):  #change name 
    user=request.user
    try:
        instance = ContractorInvoice.objects.get(id=pk)  # CHANGE model
    except ContractorInvoice.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Contractor object does not exist'}, status=404)
    

    allow,msg= check_user(request,ContractorInvoice,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data = request.data.copy()
    request_data["invoice"] = pk

    serializer = ContractInvoiceHistorySerializer( data=request_data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=201)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='login')
def attendancereport(request):
    user=request.user
    allow,msg= check_user(request,ProjectSubContractLabourAttendence,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    projectsubcontract = ProjectSubContract.objects.filter(company=request.user.company).order_by("-id")
    contractors =Contractor.objects.filter(company=request.user.company).order_by("-id")
    querysets = ProjectSubContractLabourAttendence.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,ProjectSubContractLabourAttendence,querysets)    #change, model
    context= {'queryset': queryset,"location":"proattendance","pages" :pages,"search":search,'projectsubcontract':projectsubcontract,"contractor":contractors}   #change location name 
    return render(request, 'attendance/proattendance.html',context)


@api_view(['POST'])
@login_required(login_url='login')
def add_attendancereport(request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,ProjectSubContractLabourAttendence,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    request_data=request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id
    serializer = ProjectSubContractLabourAttendenceSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    


@api_view(['PUT'])
@login_required(login_url='login')
def update_attendancereport(request, pk):  # CHANGE name
    user=request.user 
    if pk ==0:
        request_data=request.POST.copy().dict()
        if user.admin:
            request_data['company'] = user.company.id
        serializer = ProjectSubContractLabourAttendenceSerializer(data=request_data)   # CHANGE serializer
        if serializer.is_valid():  
            serializer.save()
            return JsonResponse( serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    try:
        instance = ProjectSubContractLabourAttendence.objects.get(id=pk)  # CHANGE model
    except ProjectSubContractLabourAttendence.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Item does not exist'}, status=404)    
    
    allow,msg= check_user(request,ProjectSubContractLabourAttendence,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = ProjectSubContractLabourAttendenceSerializer(instance, data=request.data,partial=True)  
     # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 

@api_view(['DELETE'])
@login_required(login_url='login')
def delete_attendancereport(request,pk):
    user=request.user
    try:
        instance = ProjectSubContractLabourAttendence.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,ProjectSubContractLabourAttendence,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except ProjectSubContractLabourAttendence.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    

from django.db.models import Q
from .utils import PaginationAndFilter


@api_view(['GET'])
@login_required(login_url='login')
def get_process_status(request):
    queryset =ProcessStatus.objects.all()
    ser =ProcessStatusSerializer(queryset,many=True)
    return Response(ser.data)


@login_required(login_url='login')
def uom(request):  #change name 
    user=request.user
    allow,msg= check_user(request,Uom,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)      
    querysets = Uom.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,Uom,querysets)    #change, model
    context= {'queryset': queryset,"location":"uom","pages" :pages,"search":search}   #change location name 
    return render(request,"library/uom.html",context)    #change template name

# @api_view(['POST'])
# @check_valid_user
# @check_user_company
# @check_admin
# @login_required(login_url='login')
# def add_uom(request):  # CHANGE name
#     user=request.user
#     allow,msg= check_user(request,Uom,instance=False)  # CHANGE model
#     if not allow:
#         return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
#     print(request.company,"company")
#     print(request.company_id ,"company_id")

#     request_data=request.POST.copy().dict()
#     if user.admin:
#         request_data['company'] = user.company.id

#     serializer = UomSerializer(data=request_data)   # CHANGE serializer
#     if serializer.is_valid():  
#         serializer.save()
#         return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
    

@api_view(['POST'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def add_uom(request):
    user = request.user
    allow, msg = check_user(request, Uom, instance=False)    
    if not allow:
        return JsonResponse({'details': msg}, status=status.HTTP_403_FORBIDDEN)      

    request_data = request.data.copy() 
    
    if user.admin:  
        request_data['company'] = user.company.id

    serializer = UomSerializer(data=request_data)  
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# @check_valid_user
# @check_user_company
# @check_admin
# @login_required(login_url='login')
# def update_uom(request, pk):  # CHANGE name
#     user=request.user
    
#     try:
#         instance = Uom.objects.get(id=pk,company = request.company)  # CHANGE model
#     except Uom.DoesNotExist:              # CHANGE model
#         return JsonResponse({'details': 'Uom object does not exist'}, status=404)
#     allow,msg= check_user(request,Uom,instance=instance)  # CHANGE model
#     if not allow:
#         return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)

#     serializer = UomSerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
#     if serializer.is_valid():  
#         serializer.save()
#         return JsonResponse( serializer.data, status=200)
#     else:
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def update_uom(request, pk):  
    user = request.user
    
    try:
        company = request.company
        if hasattr(company, '__iter__') and not isinstance(company, str):
            company = company[0] if company else None
        
        if not company:
            return JsonResponse({'details': 'Invalid or missing company reference'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance = Uom.objects.get(id=pk, company=company)  
    except Uom.DoesNotExist:              
        return JsonResponse({'details': 'Uom object does not exist'}, status=404)
    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
        return JsonResponse({'details': 'Invalid company reference'}, status=status.HTTP_400_BAD_REQUEST)
    
    allow, msg = check_user(request, Uom, instance=instance)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = UomSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['DELETE'])
@login_required(login_url='login')
def delete_uom(request,pk):
    user=request.user
    try:
        instance = Uom.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,Uom,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except Uom.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)



# def get_project_count(request):
#     # Get the current date
#     today = datetime.today()
#     current_month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     next_month_start = current_month_start.replace(month=current_month_start.month + 1)
#     current_month_end = next_month_start - timedelta(days=1)
    
#     previous_month_end = current_month_start - timedelta(days=1)
#     previous_month_start = previous_month_end.replace(day=1)

#     if request.user.is_authenticated:
#         # Calculate project count for the current month
#         current_month_project_count = Project.objects.filter(
#             company=request.user.company,
#             start_date__range=[current_month_start, current_month_end]
#         ).count()

#         # Calculate project count for the previous month
#         previous_month_project_count = Project.objects.filter(
#             company=request.user.company,
#             start_date__range=[previous_month_start, previous_month_end]
#         ).count()

#         project_counts = {
#             'current_month_project_count': current_month_project_count,
#             'previous_month_project_count': previous_month_project_count
#         }
#     else:
#         project_counts = None

#     return project_counts


# @api_view(['GET'])
# def count_api(request):
#     # Get project counts
#     project_counts_data = get_project_count(request)
#     if project_counts_data:
#         return JsonResponse(project_counts_data)
#     else:
#         return Response({'error': 'User is not authenticated'}, status=401)


# --------------------------- attendence -----------------------------------------------------


# labour attendence

@login_required(login_url='login')
def companylabour_attendance(request):
    user=request.user
    allow,msg= check_user(request,ProjectLabourAttendence,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    project=Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id")
    projectsubcontractor = CompanyLabours.objects.filter(company=request.user.company, disable=False).order_by("-id")
    querysets = ProjectLabourAttendence.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,ProjectLabourAttendence,querysets)    #change, model
    context= {'queryset': queryset,"location":"company-labour-attendance","pages" :pages,"search":search,'projectsubcontractor':projectsubcontractor,"project":project}   #change location name 
    return render(request, 'attendance/companylabourattendance.html',context)


@api_view(['POST'])
@login_required(login_url='login')
def add_companylabourattendance(request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,ProjectLabourAttendence,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    request_data=request.POST.copy().dict()
    if user.admin:
     request_data['company'] = user.company.id

    labour_id =   request_data['labour']
        
    if not labour_id:
        return JsonResponse({'labour':['This field is required']}, status=400)
    date_str = request_data.get('date')
    date_format = "%Y-%m-%d"

    try:
        date = datetime.strptime(date_str, date_format)
    except ValueError:
        return JsonResponse({'date': ['Invalid date format']}, status=400)

    attn=ProjectLabourAttendence.objects.filter(labour__id=labour_id, date=date)
    print(attn)
    if ProjectLabourAttendence.objects.filter(labour__id=labour_id, date=date).exists():
        return JsonResponse({'details': [clocked_in_message]}, status=409)

    serializer = ProjectLabourAttendenceSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    


@api_view(['PUT'])
@login_required(login_url='login')
def update_companylabourattendance(request, pk):  # CHANGE name
    user=request.user
    try:
        instance = ProjectLabourAttendence.objects.get(id=pk)  # CHANGE model
    except ProjectLabourAttendence.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Item does not exist'}, status=404)    
    allow,msg= check_user(request,ProjectLabourAttendence,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = ProjectLabourAttendenceSerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 

@api_view(['DELETE'])
@login_required(login_url='login')
def delete_companylabourattendance(request,pk):
    user=request.user
    try:
        instance = ProjectLabourAttendence.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,ProjectLabourAttendence,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except ProjectLabourAttendence.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    

from django.db.models import Q
from .utils import PaginationAndFilter
@api_view(['GET'])
@login_required(login_url='login')
def companylabourattendancelist(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,ProjectLabourAttendence,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
 
    contractors = ProjectLabourAttendence.objects.filter(company=request.user.company).order_by("-id")   #change query
    
    # current_date = date.today()

    # contractors = ProjectSubContract.objects.all()
    querysets = contractors
    pk= int(pk)
    if pk !=0:   
        querysets =querysets.filter(labour__id =pk)

    return PaginationAndFilter(querysets, request,ProjectLabourAttendenceSerializer,date_field ="date")

# employee xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
@login_required(login_url='login')
def employee_attendance(request):
    user=request.user
    allow,msg= check_user(request,ProjectLabourAttendence,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    employee =Employee.objects.filter(company=request.user.company,user__disable = False).order_by("-id")

    project=Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id")
    # projectsubcontractor = CompanyLabours.objects.filter(company=request.user.company).order_by("-id")
    # querysets = ProjectLabourAttendence.objects.filter(company=request.user.company).order_by("-id")   #change query
    # queryset,pages,search =customPagination(request,ProjectLabourAttendence,querysets)    #change, model
    # context= {'queryset': queryset,"location":"employee-labour-attendance","pages" :pages,"search":search,'projectsubcontractor':projectsubcontractor,"project":project}   #change location name 
    context ={"employee":employee, "project":project}
    return render(request, 'attendance/employee.html',context)


@api_view(['POST'])
@login_required(login_url='login')
def add_employeeattendance(request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,Attendance,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    request_data=request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id

    employee_id =   request_data['employee']


    # employee_id = user.employee.id if user.employee else  employee_id
        
    if not employee_id:
        return JsonResponse({'employee':['This field is required']}, status=400)
    date_str = request_data.get('date') 
    date_format = "%Y-%m-%d"

    try:
        date = datetime.strptime(date_str, date_format)
    except ValueError:
        return JsonResponse({'date': ['Invalid date format']}, status=400)

    attn=Attendance.objects.filter(employee__id=employee_id, date=date)
    print(attn)
    if attn.exists():
        return JsonResponse({'details': [clocked_in_message]}, status=409)

    serializer = AttendenceSerialiser(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



@api_view(['POST'])
@login_required(login_url='login')
def employee_clock_in(request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,Attendance,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    request_data=request.POST.copy().dict()
    if user.admin or user.employee:
        request_data['company'] = user.company.id

    employee_id = user.employee.id if user.employee else None
        
    if not employee_id:
        return JsonResponse({'employee':['This field is required']}, status=400)
    date_str = get_today()
    request_data['employee'] = employee_id
    # date_format = "%Y-%m-%d"

    # try:
    #     date = datetime.strptime(date_str, date_format)
    # except ValueError:
    #     return JsonResponse({'date': ['Invalid date format']}, status=400)
    request_data ['date'] =date_str
    attn=Attendance.objects.filter(employee__id=employee_id, date=date_str)
    if attn.exists():
        return JsonResponse({'details': [clocked_in_message]}, status=409)

    serializer = AttendenceSerialiser(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


@api_view(['PUT',"GET"])
@login_required(login_url='login')
def employee_clock_out(request,pk):  # CHANGE name
    user=request.user
     
    allow,msg= check_user(request,AttendenceSerialiser,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':   
        attn =Attendance.objects.filter(employee = user.employee,date =get_today()).last()
        if attn:
            serializer = AttendenceSerialiser(attn,many=False)
        else :
            serializer= EmployeeAttendenceSerialiser(user.employee,many=False)
    else:
        try:
            instance = Attendance.objects.get(id=pk)  # CHANGE model
        except Attendance.DoesNotExist:              # CHANGE model
            return JsonResponse({'details': 'Item does not exist'}, status=404)  
        serializer = AttendenceSerialiser(instance, data=request.data,partial=True)   # CHANGE Serializer
        if serializer.is_valid():  
            serializer.save()
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse( serializer.data, status=200)
    # else:
    #     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
@login_required(login_url='login')
def update_employeeattendance(request, pk):  # CHANGE name
    user=request.user
    try:
        instance = Attendance.objects.get(id=pk)  # CHANGE model
    except Attendance.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Item does not exist'}, status=404)    
    allow,msg= check_user(request,AttendenceSerialiser,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = AttendenceSerialiser(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 

@api_view(['DELETE'])
@login_required(login_url='login')
def delete_employeeattendance(request,pk):
    user=request.user
    try:
        instance = Attendance.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,Attendance,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except Attendance.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    

from django.db.models import Q
from .utils import PaginationAndFilter
@api_view(['GET'])
@login_required(login_url='login')
def employeeattendancelist(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,Attendance,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
 
    querysets = Attendance.objects.filter(company=request.user.company).order_by("-id")   #change query
    
  
    pk= int(pk)
    if pk !=0:   
        querysets =querysets.filter(employee__id =pk)

    return PaginationAndFilter(querysets, request,AttendenceSerialiser,date_field ="date")




@api_view(['GET'])
@login_required(login_url='login')
def employee_attendence_list(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,Employee,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    
    company,_=get_user_company(user)
    pk= int(pk)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if pk !=0:   
        # print(Attendance.objects.filter(employee__id = pk,company__in=company))
        querysets =Attendance.objects.filter(employee__id = pk,company__in=company)
        return PaginationAndFilter(querysets, request,AttendenceSerialiser,date_field ="date")
    
    if end_date or start_date:
        querysets =Attendance.objects.filter(company__in=company)
        return PaginationAndFilter(querysets, request,AttendenceSerialiser,date_field ="date")
        
    querysets =Employee.objects.filter(company__in=company,user__disable = False).order_by('-id')
    return PaginationAndFilter(querysets, request,EmployeeAttendenceSerialiser,date_field ="date")


@api_view(['POST'])
@login_required(login_url='login')
def make_employee_present(request,pk):
    user=request.user
    allow,msg= check_user(request,Attendance,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context) 
    
    company,_=get_user_company(user)
    date = request.POST.get('date',None)
    project_id = request.POST.get('project',None)
    clock_in = request.POST.get('clock_in',None)
    employee = request.POST.get('employee',None)

    over_time = request.POST.get('over_time',None)
    clock_out = request.POST.get('clock_out',None)
    instance =request.POST.get('instance',None)

    # update
    if pk !=0:
        proj_labr_attn = get_object_or_404(Attendance,id=pk)
        ser = AttendenceSerialiser(proj_labr_attn,request.data,context={'request':request},partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors,status=400)

    if not employee:
        return JsonResponse({"employee":["This Field is required"]},status=400)

   
    request_data =post_data(request,get_company_id(company))
    request_data['employee'] = employee

    date = date if date else get_today()
    atten = Attendance.objects.filter(employee__id=employee,date=date).last()
    if atten:
        return JsonResponse({"employee":["Already Data exists"]},status=400)
    # write custom logic for employee present for that day and throw error employee is present that day 
    ser =AttendenceSerialiser(data=request_data,context={'request':request})
    if ser.is_valid():
        ser.save()
        return Response(ser.data,status=200)
    return Response(ser.errors,status=400)
   




# --------------------------------------- registrtion ------------------------------------

@api_view(['POST'])
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
        pin = request.data.get('pin')  # Retrieve PIN from request data
        
        # Authenticate the user with phone number and password
        user = authenticate(request, phone_number=phone_number, password=password)

        print(type(user.pin),type(pin))
        
        if user is not None:
            # Check if PIN is provided and is correct
            if pin and user.pin == str(pin):
                # PIN is correct, generate token
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            elif pin:
                # PIN is incorrect
                return Response({'error': 'Invalid PIN'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # PIN is not provided, return error
                return Response({'error': 'PIN is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def reset_pin(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')
        new_pin = request.data.get('new_pin')
        otp_entered = request.data.get('otp')
        if not (phone_number and new_pin and otp_entered):
            return JsonResponse({'error': 'Phone number, OTP, and new PIN are required in the request'}, status=400)
  
        # Retrieve the user
        user = get_object_or_404(CustomUser, phone_number=phone_number)

        # Verify OTP
        otp_instances = OTP.objects.filter(user=user, otp=otp_entered)
        if not otp_instances.exists():
            return JsonResponse({'error': 'Invalid OTP'}, status=400)
        elif otp_instances.count() > 1:
            # More than one OTP object returned, handle this case accordingly
            # For example, you might want to delete all OTP instances and proceed
            otp_instances.delete()
            return JsonResponse({'error': 'Multiple OTPs found. Please try again.'}, status=400)

        # Change the PIN
        user.pin = new_pin
        user.save()

        # Delete the used OTP from the OTP table
        otp_instances.delete()

        return JsonResponse({'message': 'PIN reset successfully'})
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
        
@api_view(['POST'])
def generate_otp(request):
    phone_number = request.data.get('phone_number')
    if not phone_number:
        return JsonResponse({'error': 'Phone number is required in the request'}, status=400)
    user = get_object_or_404(CustomUser, phone_number=phone_number)
    #generated_otp = ''.join(random.choices(string.digits, k=6))
    generated_otp=1234
    otp_instance = OTP.objects.create(user=user, otp=generated_otp)
    return JsonResponse({'otp': generated_otp, 'message': 'OTP sent successfully'})

@api_view(['POST'])
def verify_otp(request):
    phone_number = request.data.get('phone_number')
    otp_entered = request.data.get('otp')

    if not (phone_number and otp_entered):
        return JsonResponse({'error': 'Phone number and OTP are required in the request'}, status=400)

    user = get_object_or_404(CustomUser, phone_number=phone_number)
    
    # Retrieve all OTP objects associated with the user and order them by created_at in descending order
    otp_queryset = OTP.objects.filter(user=user).order_by('-created_at')

    try:
        # Try to retrieve the latest OTP object from the queryset
        user_otp = otp_queryset.first()
    except OTP.DoesNotExist:
        return JsonResponse({'error': 'No OTP object found for the user'}, status=400)

    # Compare the entered OTP with the OTP stored in the OTP object
    if otp_entered == user_otp.otp:
        return JsonResponse({'message': 'OTP verification successful'})
    else:
        return JsonResponse({'error': 'Invalid OTP'}, status=400)

@api_view(['POST'])
def reset_confirm(request):
    phone_number = request.data.get('phone_number')
    otp = request.data.get('otp')
    new_pin = request.data.get('new_pin')

    if not (phone_number and otp and new_pin):
        return JsonResponse({'error': 'Phone number, OTP, and new PIN are required in the request'}, status=400)

    # Check if the user exists based on the provided phone number
    user = get_object_or_404(CustomUser, phone_number=phone_number)

    # Check if the user has a valid OTP stored
    try:
        user_otp = OTP.objects.get(user=user)
    except OTP.DoesNotExist:
        return JsonResponse({'error': 'No OTP found for the provided phone number'}, status=400)

    # Verify OTP
    if otp == user_otp.otp:
        # OTP verification successful, reset PIN
        user.pin = new_pin
        user.save()

        # Clear the used OTP
        user_otp.delete()

        return JsonResponse({'message': 'reset  confirm successfully'})
    else:
        return JsonResponse({'error': 'Invalid OTP'}, status=400)

@api_view(['POST'])
def login_with_token_and_pin(request):
    if request.method == 'POST':
        token_key = request.data.get('token')
        pin = request.data.get('pin')

        # Authenticate the user using the provided token
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user's PIN matches the provided PIN
        if user.pin == pin:
            # PIN is correct, generate a new token
            new_token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': new_token.key}, status=status.HTTP_200_OK)
        else:
            # PIN is incorrect
            return Response({'error': 'Invalid PIN'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    




# ------------------------------------------- azar


@api_view(['GET'])
@login_required(login_url='login')
def purchase_list(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,PurchaseInvoice,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
 
    querysets = PurchaseInvoice.objects.filter(company=request.user.company).order_by("-id")   #change query
   
    pk= int(pk)
    if pk !=0:   
        print('vendor')
        querysets = querysets.filter(vendor__id = pk)    

    project_id = request.GET.get('project')

    # try :
    #     project =int(project_id)
    # except:
    #     project =0

    project =get_int_or_zero(project_id)

    if project and project !=0:
        querysets =querysets.filter(site__id =project)

    # Apply pagination and get the serialized data
    paginated_data = PaginationAndFilter(querysets, request, PurchaseInvoiceListSerializer, date_field="created_at")

    results = paginated_data.data['results']
    
    # Calculate total amounts
    total_purchase_amount = sum(get_amount_or_zero(item['total_amount'] )for item in results)
    total_purchase_paid_amount = sum(get_amount_or_zero(item['paid']) for item in results)
    
    # Add totals to the response data
    paginated_data.data['total_purchase_amount'] = total_purchase_amount
    paginated_data.data['total_purchase_paid_amount'] = total_purchase_paid_amount
    
    return paginated_data

    return PaginationAndFilter(querysets, request,PurchaseInvoiceListSerializer,date_field ="created_at")


@api_view(['GET'])
@login_required(login_url='login')
def quatation_list(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,Quatation,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
 
    querysets = Quatation.objects.filter(company=request.user.company).order_by("-id")   #change query
    
    pk= int(pk)
    if pk !=0:   
        querysets =querysets.filter(site__id =pk)


    return PaginationAndFilter(querysets, request,QuatationListSerializer,date_field ="start_date")


# ------------------------------------------------ SALARY lIST ------------------------------



@api_view(['GET'])
# @permission_classes([AllowAny])
@login_required(login_url='login')
def employee_salary_list(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,Employee,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)   
    company,_=get_user_company(user)
    querysets =Employee.objects.filter(company__in=company,user__disable = False)

    pk= int(pk)
    if pk !=0:   
        querysets =querysets.filter(id =pk)
    return PaginationAndFilter(querysets, request,EmployeeSalarySerializer,date_field ="start_date")


@api_view(['GET'])
# @permission_classes([AllowAny])
@login_required(login_url='login')
def profit_and_loss(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,Project,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)  
    company,_=get_user_company(user)  
    querysets =Project.objects.filter(company__in=company, is_disabled=False)
    return PaginationAndFilter(querysets, request,ProfitandLoseSerializer,date_field ="start_date")




@api_view(['GET'])
# @permission_classes([AllowAny])
@login_required(login_url='login')
def labour_salary_list(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,Employee,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    company,_=get_user_company(user)
    querysets =CompanyLabours.objects.filter(company__in=company)

    pk= int(pk)
    if pk !=0:   
        querysets =querysets.filter(id =pk)
    return PaginationAndFilter(querysets, request,CompanyLabourSalarySerializer,date_field ="start_date")
    


# --------------------------------------------------------

@api_view(['GET'])
# @permission_classes([AllowAny])
@login_required(login_url='login')
def labour_attendence_list(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,Employee,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    
    company,_=get_user_company(user)

    project_id = request.GET.get('project')

    try:
        pk = int(pk)
    except ValueError:
        return JsonResponse({'error': 'Invalid pk'}, status=400)

    # Get the project if project_id is provided
    if project_id:
        try:
            project_id = int(project_id)
        except ValueError:
            project_id = None
    else:
        project_id = None

    
    if pk !=0:   
        querysets =ProjectLabourAttendence.objects.filter(labour__id =pk,company__in=company)
        return PaginationAndFilter(querysets, request,ProjectLabourAttendenceSerializer,date_field ="date")
    
    if pk ==0 and project_id  :  
        querysets =ProjectLabourAttendence.objects.filter(project__id =project_id,company__in=company)
        return PaginationAndFilter(querysets, request,ProjectLabourAttendenceSerializer,date_field ="date")
        
    querysets =CompanyLabours.objects.filter(company__in=company)
    return PaginationAndFilter(querysets, request,LabourAttendenceSerialiser,date_field ="date")




@api_view(['POST'])
@check_valid_user
@check_user_company
@login_required(login_url='login')
def make_labour_present(request,pk):
    user=request.user
    allow,msg= check_user(request,ProjectLabourAttendence,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context) 
    
    company,_=get_user_company(user)
    date = request.POST.get('date',None)
    project_id = request.POST.get('project',None)
    clock_in = request.POST.get('clock_in',None)
    labour = request.POST.get('labour',None)

    over_time = request.POST.get('over_time',None)
    clock_out = request.POST.get('clock_out',None)
    instance =request.POST.get('instance',None)

    # update
    if pk !=0:
        proj_labr_attn = get_object_or_404(ProjectLabourAttendence,id=pk)
        ser = ProjectLabourAttendenceSerializer(proj_labr_attn,request.data,context={'request':request},partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors,status=400)

    if not labour:
        return JsonResponse({"labour":["This Field is required"]},status=400)

    date = date if date else get_today()
   
    request_data =post_data(request,get_company_id(company))
    request_data['labour'] = labour
    proj_labr_attn = ProjectLabourAttendence.objects.filter(labour__id=labour,date=date).last()
    if proj_labr_attn:
        return JsonResponse({"labour":["Already Data exists"]},status=400)
    ser =ProjectLabourAttendenceSerializer(data=request_data,context={'request':request})
    if ser.is_valid():
        ser.save()
        return Response(ser.data,status=200)
    return Response(ser.errors,status=400)
   

# # project subcontract attendence
@api_view(['GET'])
@login_required(login_url='login')
def attendancelist(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,ProjectSubContractLabourAttendence,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
 
    contractor = request.GET.get('contarctor')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    company,_=get_user_company(user)
    pk= int(pk)
    if pk !=0 or contractor !="0" or start_date or end_date:   
        querysets = ProjectSubContractLabourAttendence.objects.filter(company__in=company).order_by("-id") 
        if pk!=0:
            querysets = querysets.filter(contract__id  =pk,company__in=company)
        if contractor !="0":
            querysets =querysets.filter(contract__contractor__id =int(contractor),)
        return PaginationAndFilter(querysets, request,ProjectSubContractLabourAttendenceSerializer,date_field ="date")
        
    querysets =ProjectSubContract.objects.filter(company__in=company)
    return PaginationAndFilter(querysets, request,ProjectSubContractAttendenceSerialiser,date_field ="created_at")

@api_view(['GET'])
@login_required(login_url='apilogin')
def attendancelistpro(request, pk):  # Change name
    user = request.user
    allow, msg = check_user(request, ProjectSubContractLabourAttendence, instance=False)  # CHANGE model
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)

    contractor = request.GET.get('contractor')  # Corrected spelling
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    project_id = request.GET.get('project')  # Retrieve project ID

    company, _ = get_user_company(user)
    pk = int(pk)
    if pk != 0 or contractor != "0" or start_date or end_date or project_id:  # Check if any filter is provided
        querysets = ProjectSubContractLabourAttendence.objects.filter(company__in=company).order_by("-id")
        if pk != 0:
            querysets = querysets.filter(contract__id=pk, company__in=company)
        if contractor != "0":
            querysets = querysets.filter(contract__contractor__id=int(contractor))
        if project_id:  # If project ID is provided, filter by project
            querysets = querysets.filter(contract__project__id=int(project_id))
        if start_date:
            querysets = querysets.filter(date__gte=start_date)
        if end_date:
            querysets = querysets.filter(date__lte=end_date)
        return PaginationAndFilter(querysets, request, ProjectSubContractLabourAttendenceSerializer, date_field="date")

    querysets = ProjectSubContract.objects.filter(company__in=company)
    return PaginationAndFilter(querysets, request, ProjectSubContractAttendenceSerialiser, date_field="created_at")




@login_required(login_url='login')
def pettycash(request):  #change name 
    user=request.user
    allow,msg= check_user(request,PettyCash,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
      
    querysets = PettyCash.objects.filter(company=request.user.company).order_by("-id") 
    employee = Employee.objects.filter(company=request.user.company,user__disable = False).order_by("-id") 
    site_location =Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id")   #change query
    payment_method = PaymentMethod.objects.all().order_by("-id")
    queryset,pages,search =customPagination(request,PettyCash,querysets)    #change, model
    context= {'queryset': queryset,
              "location":"pettycash",
              "pages" :pages,
              "employees":employee,
              "site_locations": site_location,
              "search":search,
              "payment_method":payment_method,
              }   #change location name 
    return render(request,"expense/pettycash.html",context)    #change template name


@api_view(['GET'])
@login_required(login_url='apilogin')
def pettycash_list(request, pk=None):
    user_company = request.user.company

    if pk:
        try:
            files = PettyCash.objects.get(pk=pk, company=user_company)
        except PettyCash.DoesNotExist:
            return Response({'error': 'This id not Valid'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PettyCashSerializer(files)
        return Response(serializer.data)
    else:
        files = PettyCash.objects.filter(company=user_company)
        if not files.exists():
            return Response({'error': 'No Petty Cash found for the specified company'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PettyCashSerializer(files, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def add_pettycash (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,PettyCash,instance=False)  # CHANGE model
    if not allow:       
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data=request.POST.copy().dict()
    attachments = request.FILES.get("attachment",None) 

    if user.admin:
        request_data['company'] = user.company.id

    if attachments: 
         request_data['attachment'] = attachments

    serializer = PettyCashSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def update_pettycash(request, pk):
    user = request.user

    try:
        instance = PettyCash.objects.get(id=pk)
    except PettyCash.DoesNotExist:
        return JsonResponse({'detail': 'Item does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    # Assuming check_user verifies that the user can update this specific PettyCash entry
    allow, msg = check_user(request, PettyCash, instance=instance)
    if not allow:
        return JsonResponse({'detail': msg}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = PettyCashSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@login_required(login_url='login')
def delete_pettycash(request,pk):
    user=request.user
    try:
        instance = PettyCash.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,PettyCash,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except PettyCash.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    
# def clientcash(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     payment_methods = PaymentMethod.objects.all()  # Get all payment methods
#     payment_history = PaymentHistory.objects.filter(project=project)  # Get payment history for this project

#     total_paid_amount = payment_history.aggregate(total_paid=Sum('payment_amount'))['total_paid']
#     total_paid_amount = total_paid_amount if total_paid_amount else 0
    
#     # Calculate pending amount
#     pending_amount = project.estimation - total_paid_amount
    


#     client_name = project.client
#     contact_no = project.contact_no

#     context = {
#         'client_name': client_name,
#         'contact_no': contact_no,
#         'project': project , 'payment_methods': payment_methods, 'payment_history': payment_history,'total_paid_amount': total_paid_amount,
#         'pending_amount': pending_amount
#     }

#     return render(request, 'project\clientcash.html', context)

def clientcash(request, pk):
    project = get_object_or_404(Project, pk=pk)
    payment_methods = PaymentMethod.objects.all()
    payment_history = PaymentHistory.objects.filter(project=project)
    
    total_paid_amount = payment_history.aggregate(total_paid=Sum('payment_amount'))['total_paid']
    total_paid_amount = total_paid_amount if total_paid_amount else 0
    pending_amount = project.estimation - total_paid_amount

    client_name = project.client
    contact_no = project.contact_no

    context = {
        'client_name': client_name,
        'contact_no': contact_no,
        'project': project,
        'payment_methods': payment_methods,
        'payment_history': payment_history,
        'total_paid_amount': total_paid_amount,
        'pending_amount': pending_amount,
    }

    return render(request, 'project/clientcash.html', context)

# API view
# @api_view(['GET', 'POST'])
# def clientcashpay(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     payment_history = PaymentHistory.objects.filter(project=project)
    
#     if request.method == 'POST':
#         data = request.data.copy()
#         data['project'] = project.id  # Set the project field
#         serializer = PaymentHistorySerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     return Response("This endpoint only supports POST requests.", status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST'])
def clientcashpay(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'GET':
        payment_history = PaymentHistory.objects.filter(project=project)
        serializer = PaymentHistorySerializer(payment_history, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()  # Copy request data to modify
        data['project'] = project.id  # Assign project ID to data

        img = request.FILES.get("img",None)

        if img:
          data['img'] = img 

        serializer = PaymentHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PUT'])
def update_clientcashpay(request, payment_id):
    try:
        payment_history_instance = get_object_or_404(PaymentHistory, pk=payment_id)
    except PaymentHistory.DoesNotExist:
        return Response("Payment history not found", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PaymentHistorySerializer(payment_history_instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response("Unsupported method", status=status.HTTP_405_METHOD_NOT_ALLOWED)


#--------------------------------------Daily Task-----------------------------------

# @api_view(['GET'])
# @login_required(login_url='login')
# def dailytask_list(request):
#     user=request.user
#     allow,msg= check_user(request,Dailytask,instance=False)  # CHANGE model
#     if not allow:
#          context ={"unauthorized":msg}
#          return render(request,"login.html",context)    
     
#     querysets = Dailytask.objects.filter(company=request.user.company).order_by("-id")
#     project = request.GET.get('project')
#     project_id =get_int_or_zero(project)
#     if project_id:
#         querysets =querysets.filter(project__id = project_id)
#     ser = dailyTaskSerializer(querysets,many=True)
#     return Response (ser.data)

@api_view(['GET'])
@login_required(login_url='login')
def dailytask_list(request, project_id=None):
    user = request.user
    allow, msg = check_user(request, Dailytask, instance=False)
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)

    querysets = Dailytask.objects.filter(company=user.company).order_by("-id")
    
    # Filter by project_id if provided
    if project_id is not None:
        querysets = querysets.filter(project__id=project_id)
    
    ser = dailyTaskSerializer(querysets, many=True)
    return Response(ser.data)



@login_required(login_url='login')
def dailytask(request):  #change name 
    user=request.user
    allow,msg= check_user(request,Dailytask,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
      
    querysets = Dailytask.objects.filter(company=request.user.company).order_by("-id")
    project = Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id") 
    subcontract =ProjectSubContract.objects.filter(company=request.user.company).order_by("-id")
    # subcontract_item =ProjectSubContractUnitRates.objects.all().order_by("-id")
    uom =Uom.objects.filter(company=request.user.company).order_by("-id")
    queryset,pages,search =customPagination(request,Dailytask,querysets)    #change, model
    context= {'queryset': queryset,
              "location":"dailytask",
              "pages" :pages,
              "projects":project,   
              "subcontracts":subcontract,
              "uoms": uom,
              "search":search,
              }   #change location name 
    return render(request,"dailytask.html",context)    #change template name

@api_view(['GET'])
@login_required(login_url='apilogin')
def dailytasks_list(request, pk=None):
    user_company = request.user.company  

    if pk:
        try:
            task = Dailytask.objects.get(pk=pk, company=user_company)
        except Dailytask.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = dailyTaskSerializer(task)
        return Response(serializer.data)
    else:
        task = Dailytask.objects.filter(company=user_company)
        serializer = dailyTaskSerializer(task, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
@check_valid_user
@check_user_company
@login_required(login_url='login')
def add_dailytask (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,Dailytask,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data=request.POST.copy().dict()

    if user.admin or user.employee:
        request_data['company'] = user.company.id


    serializer = dailyTaskSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@check_valid_user
@check_user_company
@login_required(login_url='login')
def update_dailytask(request, pk):  # CHANGE name
    user=request.user

    try:
        instance = Dailytask.objects.get(id=pk)  # CHANGE model
    except Dailytask.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)

    allow,msg= check_user(request,Dailytask,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = dailyTaskSerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@login_required(login_url='login')
def delete_dailytask(request,pk):
    user=request.user
    try:
        instance = Dailytask.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,Dailytask,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except Dailytask.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    
#-------------------------------------------------> Employee Site Allocation <---------------------------------------

@login_required(login_url='login')
def site_allocation(request):
    user=request.user
    allow,msg= check_user(request,SiteAllocation,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    employee =Employee.objects.filter(company=request.user.company,user__disable = False    ).order_by("-id")

    project=Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id")
    context ={"employee":employee, "project":project}
    return render(request, 'site_allocation/emp_site_allocation.html',context)

@api_view(['GET'])
@login_required(login_url='login')
def site_allocation_list(request, pk):  # change name 
    user = request.user
    allow, msg = check_user(request, SiteAllocation, instance=False)  # CHANGE model
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)    
    
    company, _ = get_user_company(user)
    pk = int(pk)

    if pk != 0:
        querysets = SiteAllocation.objects.filter(employee__id=pk, company__in=company).exclude(employee__isnull=True)
        return PaginationAndFilter(querysets, request, SiteAllocationEmployeeSerializer, date_field="date")
    
    querysets = SiteAllocation.objects.filter(company__in=company).exclude(employee__isnull=True).order_by('-id')
    return PaginationAndFilter(querysets, request, SiteAllocationEmployeeSerializer, date_field="date")

@api_view(['POST'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def add_site_allocation(request):
    user = request.user
    allow, msg = check_user(request, SiteAllocation, instance=False)
    
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data = request.POST.copy().dict()
    
    if user.admin:
        request_data['company'] = user.company.id
    
    serializer = SiteAllocationEmployeeSerializer(data=request_data)
    
    if serializer.is_valid():
        site_allocation = serializer.save(created_by=user)
        return JsonResponse(SiteAllocationEmployeeSerializer(site_allocation).data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT'])
# @check_valid_user
# @check_user_company
# @check_admin
# @login_required(login_url='login')
# def site_allocationemployee(request, pk):  
#     if request.method == 'PUT':
#         try:
#             site_allocation = SiteAllocation.objects.get(pk=pk)
#         except SiteAllocation.DoesNotExist:
#             return Response({'detail': 'Site allocation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = SiteAllocationEmployeeSerializer(site_allocation, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def site_allocationemployee(request, pk):  
    # Check user permissions
    user = request.user
    allow, msg = check_user(request, SiteAllocation, instance=False)
    if not allow:
        return Response({'detail': msg}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'PUT':
        try:
            site_allocation = SiteAllocation.objects.get(pk=pk)
        except SiteAllocation.DoesNotExist:
            return Response({'detail': 'Site allocation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check user permissions for the specific object
        allow, msg = check_user(request, site_allocation)
        if not allow:
            return Response({'detail': msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = SiteAllocationEmployeeSerializer(site_allocation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # For the GET method
    try:
        site_allocation = SiteAllocation.objects.get(pk=pk)
    except SiteAllocation.DoesNotExist:
        return Response({'detail': 'Site allocation not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check user permissions for the specific object
    allow, msg = check_user(request, site_allocation)
    if not allow:
        return Response({'detail': msg}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = SiteAllocationEmployeeSerializer(site_allocation)
    return Response(serializer.data)

    
@api_view(['DELETE'])
@login_required(login_url='login')
def delete_site_allocation_list(request, pk):
    try:
        site = SiteAllocation.objects.get(id=pk)
        allow, msg = check_user(request, SiteAllocation, instance=site)
        if not allow:
            return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
        site.delete()
        return JsonResponse({'details': 'Site allocation deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except SiteAllocation.DoesNotExist:
        return JsonResponse({'details': 'Site allocation does not exist'}, status=status.HTTP_404_NOT_FOUND)


#-------------------------------------------------> Labour Site Allocation <---------------------------------------

@login_required(login_url='login')
def lab_site_allocation(request):
    user=request.user
    allow,msg= check_user(request,SiteAllocation,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    employee =CompanyLabours.objects.filter(company = request.user.company, disable=False).order_by("-id")

    #company=request.user.company,user__disable = False

    project=Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id")
    context ={"employee":employee, "project":project}
    return render(request, 'site_allocation/lab_site_allocation.html',context)

@api_view(['GET'])
@login_required(login_url='login')
def lab_site_allocation_list(request, pk):  # change name 
    user = request.user
    allow, msg = check_user(request, SiteAllocation, instance=False)  # CHANGE model
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)    
    
    company, _ = get_user_company(user)
    pk = int(pk)

    if pk != 0:
        querysets = SiteAllocation.objects.filter(labour__id=pk, company__in=company).exclude(labour__isnull=True)
        return PaginationAndFilter(querysets, request, SiteAllocationLabourSerializer, date_field="date")
    
    querysets = SiteAllocation.objects.filter(company__in=company).exclude(labour__isnull=True).order_by('-id')
    return PaginationAndFilter(querysets, request, SiteAllocationLabourSerializer, date_field="date")
    
@api_view(['POST'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def add_lab_site_allocation(request):
    user = request.user
    allow, msg = check_user(request, SiteAllocation, instance=False)
    
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data = request.POST.copy().dict()
    
    if user.admin:
        request_data['company'] = user.company.id
    
    serializer = SiteAllocationLabourSerializer(data=request_data)
    
    if serializer.is_valid():
        site_allocation = serializer.save(created_by=user)
        return JsonResponse(SiteAllocationLabourSerializer(site_allocation).data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET', 'PUT'])
# @login_required(login_url='login')
# def site_allocationlabour(request, pk):  
#     if request.method == 'PUT':
#         try:
#             site_allocation = SiteAllocation.objects.get(pk=pk)
#         except SiteAllocation.DoesNotExist:
#             return Response({'detail': 'Site allocation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = SiteAllocationLabourSerializer(site_allocation, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@check_valid_user
@check_user_company
@check_admin
@login_required(login_url='login')
def site_allocationlabour(request, pk):
    # Check user permissions
    user = request.user
    allow, msg = check_user(request, SiteAllocation, instance=False)
    if not allow:
        return Response({'detail': msg}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'PUT':
        try:
            site_allocation = SiteAllocation.objects.get(pk=pk)
        except SiteAllocation.DoesNotExist:
            return Response({'detail': 'Site allocation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check user permissions for the specific object
        allow, msg = check_user(request, site_allocation)
        if not allow:
            return Response({'detail': msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = SiteAllocationLabourSerializer(site_allocation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # For the GET method
    try:
        site_allocation = SiteAllocation.objects.get(pk=pk)
    except SiteAllocation.DoesNotExist:
        return Response({'detail': 'Site allocation not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check user permissions for the specific object
    allow, msg = check_user(request, site_allocation)
    if not allow:
        return Response({'detail': msg}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = SiteAllocationLabourSerializer(site_allocation)
    return Response(serializer.data)




def purchase_details(request, purchase_id):
    purchase = get_object_or_404(PurchaseInvoice, id=purchase_id)
    items = PurchaseItems.objects.filter(invoice=purchase)
    
    # Calculate balance
    balance = purchase.total_amount - purchase.paid
    
    data = {
        'site_name': purchase.site.site_location if purchase.site else '',
        'company_name': purchase.vendor_company,
        'gst': purchase.gst if purchase.gst else '',
        'tax': str(purchase.tax),
        'contact_no': purchase.contact_no if purchase.contact_no else '',
        'invoice_id': purchase.invoice_id,
        'vendor_name': purchase.vendor.vendorname if purchase.vendor else '',
        'total_amount': str(purchase.total_amount),
        'paid': str(purchase.paid),
        'pending': str(purchase.pending),
        'balance': str(balance),  # Include balance in the response
        'created_at': purchase.created_at.strftime('%Y-%m-%d'),
        'items': [
            {
                'item_name': item.name,
                'quantity': str(item.qty),
                'unit': item.unit.name if item.unit else '',
                'amount': str(item.sub_total)
            }
            for item in items
        ],
    }
    return JsonResponse(data)

@api_view(['GET'])
@login_required(login_url='login')
def get_purchase(request, pk):
    try:
        purchase = PurchaseInvoice.objects.get(pk=pk)
    except PurchaseInvoice.DoesNotExist:
        return HttpResponseNotFound('<h1>purchase not found</h1>')

    if request.method == 'GET':
        projects = Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id") 
        vendors = VendorRegistration.objects.filter(company=request.user.company).order_by("-id") 
        items = MaterialLibrary.objects.filter(company=request.user.company).order_by("-id")
        uom = Uom.objects.filter(company=request.user.company).order_by("-id")
        inventory = InventoryStock.objects.filter(company=request.user.company).order_by("-id")
  
        context = {
            'purchase': purchase,
            'pk': pk,
            'uom': uom,
            'projects': projects,
            'vendors': vendors,
            'items': items,
            'inventory': inventory,
        }
        return render(request, 'purchase/purchasedetails.html', context)
    
@api_view(['PUT', 'GET'])
@check_valid_user
@check_user_company
@login_required(login_url='login')
def update_purchase(request, pk):
    user = request.user
    try:
        company = request.company
        if hasattr(company, '__iter__') and not isinstance(company, str):
            company = company[0] if company else None
        
        if not company:
            return JsonResponse({'details': 'Invalid or missing company reference'}, status=status.HTTP_400_BAD_REQUEST)
        purchase = PurchaseInvoice.objects.get(pk=pk, company=company)
    except PurchaseInvoice.DoesNotExist:           
        return JsonResponse({'details': 'Purchase object does not exist'}, status=404)
    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
        return JsonResponse({'details': 'Invalid company reference'}, status=status.HTTP_400_BAD_REQUEST) 

    if request.method == 'GET':
        projects = Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id") 
        vendors = VendorRegistration.objects.filter(company=request.user.company).order_by("-id") 
        items = MaterialLibrary.objects.filter(company=request.user.company).order_by("-id")
        uom = Uom.objects.filter(company=request.user.company).order_by("-id")
        inventory = InventoryStock.objects.filter(company=request.user.company).order_by("-id")
  
        context = {
            'purchase': purchase,
            'pk': pk,
            'uom': uom,
            'projects': projects,
            'vendors': vendors,
            'items': items,
            'inventory': inventory,
        }
        return render(request, 'purchase/purchaseupdate.html', context)

    if request.method == 'PUT':
        
        purchase_serializer = PurchaseInvoiceSerializer(purchase, data=request.data, partial=True)
        if not purchase_serializer.is_valid():
            return Response(purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        purchase_serializer.save()

        purchase_serializer = PurchaseInvoiceSerializer(purchase)
        return Response(purchase_serializer.data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@login_required(login_url='login')
def get_quatation(request, pk):
    try:
        quatation = Quatation.objects.get(pk=pk)
    except Quatation.DoesNotExist:
        return HttpResponseNotFound('<h1>Quatation not found</h1>')

    if request.method == 'GET':
        projects = Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id") 
        employees = Employee.objects.filter(company=request.user.company,user__disable = False).order_by("-id") 
        # status =WorkStatus.objects.filter().order_by("-id")
        uom = Uom.objects.filter(company=request.user.company).order_by("-id")
        inventory=InventoryStock.objects.filter(company=request.user.company).order_by("-id")
  
        context = {
            'quatation': quatation,
            'pk':pk,
            'uom': uom,
            'projects': projects,
            'employees': employees ,
            # 'status': status,
            'inventory': inventory,
        }
        return render(request, 'quatation/quatationdetails.html', context)

@api_view(['PUT', 'GET'])
@login_required(login_url='login')
def update_quatation(request, pk):
    try:
        quatation = Quatation.objects.get(pk=pk)
    except Quatation.DoesNotExist:
        return HttpResponseNotFound('<h1>Quatation not found</h1>')

    if request.method == 'GET':
        projects = Project.objects.filter(company=request.user.company, is_disabled=False).order_by("-id") 
        employees = Employee.objects.filter(company=request.user.company,user__disable = False).order_by("-id") 
        # status =WorkStatus.objects.filter().order_by("-id")
        uom = Uom.objects.filter(company=request.user.company).order_by("-id")
        inventory=InventoryStock.objects.filter(company=request.user.company).order_by("-id")
  
        context = {
            'quatation': quatation,
            'pk':pk,
            'uom': uom,
            'projects': projects,
            'employees': employees ,
            # 'status': status,
            'inventory': inventory,
        }
        return render(request, 'quatation/quatationupdate.html', context)

    elif request.method == 'PUT':
       quatation_serializer =  QuatationSerializer(quatation, data=request.data, partial=True)
    if not quatation_serializer.is_valid():
        return Response(quatation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    quatation_serializer.save()

    # table_data = request.data.get('table')
    # if table_data:
    #     try:
    #         table_data = json.loads(table_data)
            
    #         #PurchaseItems.objects.filter(purchase=purchase).delete()
    #         #PurchaseItems.objects.filter(invoice=purchase).delete()


    #         for data in table_data:
    #             data['quatation'] = quatation.id
    #             items_serializer = QuatationItemsSerializer(data=data)
    #             if items_serializer.is_valid():
    #                 items_serializer.save()
    #             else:
    #                 return Response(items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except json.JSONDecodeError:
    #         return JsonResponse({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(quatation_serializer.data)

def purchasetableupdate(request, id):
    item = get_object_or_404(PurchaseItems, id=id)

    if request.method == "POST":
        qty = request.POST.get('qty')
        price = request.POST.get('price')
        sub_total = request.POST.get('sub_total')
        unit_id = request.POST.get('unit')
        item_id = request.POST.get('item')
        
        # Get the UOM and Item instances
        unit = get_object_or_404(Uom, id=unit_id)
        selected_item = get_object_or_404(MaterialLibrary, id=item_id)
        
        item.qty = qty
        item.price = price
        item.sub_total = sub_total
        item.unit = unit
        item.item = selected_item
        item.save()
        
        return redirect('purchaselist')
    
    items = MaterialLibrary.objects.all()
    uom = Uom.objects.all()

    return render(request, 'purchase/purchaseupdate.html', {
        'item': item,
        'items': items,
        'uom': uom,
    })

def quatationtableupdate(request, id):
    item = get_object_or_404(QuatationItems, id=id)

    if request.method == "POST":
        qty = request.POST.get('qty')
        unit_id = request.POST.get('unit')
        item_id = request.POST.get('inventory')
        
        # Ensure the InventoryStock instance exists
        try:
            selected_item = InventoryStock.objects.get(id=item_id)
        except InventoryStock.DoesNotExist:
            return HttpResponseNotFound("Inventory stock not found")
        
        # Get the UOM instance
        unit = get_object_or_404(Uom, id=unit_id)
        
        item.qty = qty
        item.unit = unit
        item.inventory = selected_item
        item.save()
        
        return redirect('quatationlist')
    
    inventory = InventoryStock.objects.all()
    uom = Uom.objects.all()

    return render(request, 'quatation/quatationupdate.html', {
        'item': item,
        'inventory': inventory,
        'uom': uom,
    })
        # except json.JSONDecodeError:
        #     return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        # except Exception as e:
        #     return JsonResponse({'error': str(e)}, status=500)



@api_view(['GET'])
@login_required(login_url='login')    
def item_price_track(request,pk,site_or_inventory):
    if site_or_inventory ==0:
        item =get_object_or_404(InventoryStock,id=pk)
    else :
        item =get_object_or_404(SiteStock,id=pk)
    purchase_records =item.purchase_history
    serializers = PurchaseItemsPriceTrackSerializer(purchase_records,many=True)
    data = serializers.data

    item_name =item.item.item if item.item else None
    
    results={
        "data" : data,
        "item_name" :item_name
    }

    return Response(results)

@api_view(['GET'])
def get_payment_methods(request):
    payment_methods = PaymentMethod.objects.all()
    serializer = PaymentMethodSerializer(payment_methods, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_employees(request):
    employees = Employee.objects.values('id', 'name')
    employees_list = list(employees)
    return Response(employees_list)


