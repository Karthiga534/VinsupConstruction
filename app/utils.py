import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.serializers import serialize
from datetime import datetime, timedelta ,date
import string
import random
from django.utils import timezone
from rest_framework.response import Response
import os

date_format = "%Y-%m-%d"
# PAGE_SIZE = 10
PAGE_SIZE = os.getenv("PAGINATION_SIZE")

def generate_unique_identifier(self):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))



def customPagination(request,Klass,queryset,serializer_class=None):
    search_query = request.GET.get('search',"")
    if search_query:
        search_filters = Q()
        for field in Klass._meta.fields:
            if field.get_internal_type() in ['CharField', 'TextField']: 
                search_filters |= Q(**{f'{field.name}__icontains': search_query})
        
        queryset = queryset.filter(search_filters)

    paginator = Paginator(queryset, PAGE_SIZE)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages =paginator.num_pages

    obj =page_obj.object_list

    if serializer_class:
            queryjs =  (serializer_class(obj,many=True).data)
            # queryjs = json.dumps(queryjs)
            print(queryjs)

    return page_obj,pages,search_query



def check_user(request,klass,instance=False):
    msg ='not allowed'
    return True ,msg


from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def PaginationAndFilter(queryset, request,serializer_class,date_field=None):
    # # Date Filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if date_field:
        queryset =filter_by_date_range(queryset,start_date,end_date,date_field)
   
    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = PAGE_SIZE
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(paginated_queryset,context={'request': request}, many=True)

    return paginator.get_paginated_response(serializer.data)

   

   
from datetime import datetime
from django.http import JsonResponse
from django.db.models import QuerySet

def filter_by_date_range(queryset: QuerySet, start_date: str, end_date: str, date_field: str) -> QuerySet:
    # return queryset
    try:
       
        if start_date:
            # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(**{f"{date_field}__gte": start_date})

        if end_date:
            # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(**{f"{date_field}__lte": end_date})
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=400)
      

    return queryset



def filter_by_month_range(Klass,company, cms: str, cme: str,pms: str, pme: str,  date_field: str ,queryset: QuerySet = None) -> tuple:

    if isinstance(queryset, bool):
        print(queryset,Klass,"iin")
        queryset = Klass.objects.filter(company__in = company,**{f"{date_field}__range": [pms, cme]})
        # print(queryset.count())

    cm_count = queryset.filter(**{f"{date_field}__range": [cms, cme]}).count()
    pm_count = queryset.filter(**{f"{date_field}__range": [pms, pme]}).count()
    
    # Calculate the difference
    difference = cm_count - pm_count
    
    return cm_count, pm_count, difference
  



from django.db.models import Q
from datetime import datetime, timedelta

def filter_projects_by_date(Klass,company, start_date_range):
    return Klass.objects.filter(company=company, start_date__range=start_date_range)

def get_current_month():
    today = datetime.today()
    current_month_start = today.replace(day=1).date()
    next_month_start = (today.replace(day=1) + timedelta(days=32)).replace(day=1).date()
    return current_month_start, next_month_start



def get_company(user):
    company =[]
    company_msg = 'User is not associated with any company'
    if user.company :
        company = [user.company]
    elif user.owner:
        company = user.getcompanies
    else :
        company = None
    
    return company ,company_msg



from decimal import Decimal
def get_amount_or_zero(amt):
    # print(amt)
    try:
        value= Decimal(amt)
    except:
        value = 0
    return value




def get_int_or_zero(amt):
    try:
        value= int(amt)
    except:
        value = 0
    return value



def get_date(date_obj):
#    print(type(date_obj))
   return date_obj



# today date
def get_today():
    # print((timezone.now().date()),)
    return timezone.now().date()


def get_date_object(query_date):
    # print(datetime.strptime(query_date, date_format))
    return datetime.strptime(query_date, date_format).date()



def get_month_start_and_end(date):
    # print(type(date))
    month_start = date.replace(day=1)
    next_month = month_start + timedelta(days=32)
    month_end = next_month.replace(day=1) - timedelta(days=1)
    return month_start, month_end


# -------------------------------------------

def get_today_attendance_status(request,all_labours):
    from .models import CompanyLabours,ProjectLabourAttendence
    today = date.today() 

    attendance_status = []
    
    for labour in all_labours:
        attendance_record = ProjectLabourAttendence.objects.filter(
            labour=labour,
            date=today
        ).first()  # Get the first attendance record for today if it exists

        if attendance_record and attendance_record.clock_in:
            is_present = True
            clock_in_time = attendance_record.clock_in
            clock_out = attendance_record.clock_out
            overtime=attendance_record.over_time
        else:
            is_present = False
            clock_in_time = None
            clock_out =None
            overtime=None
        attendance_status.append({
            'labour_id': labour.id,
            'labour_name': labour.name, 
            'project_name': labour.name,
            'is_present': is_present,
            'clock_in': clock_in_time,
            "clock_out":clock_out,
            'overtime' :overtime,
            'date':today
        })

    return attendance_status





def get_user_company(user):
    company =[]
    company_msg = 'User is not associated with any company'

    if  user.admin :
        company = user.get_companies
    elif user.company:
        company = [user.company]
    else :
        company =[]

    return company ,company_msg

#   company,_=get_user_company(user)

def get_company_id(company_list):
    print(type(company_list))
    company_list = list(company_list)

    if company_list:
        last_company = company_list[-1]  
        print(last_company)
        # Get the last Company instance
        last_company_id = last_company.id # Get the ID of the last Company
        return last_company_id
    return None




from rest_framework.authtoken.models import Token
def generate_new_token(user):
    # Token.objects.filter(user=user).delete()
    # token = Token.objects.create(user=user)
    token, _ = Token.objects.get_or_create(user=user)
    return token


# send sms

import requests

BASE_SMS ="http://pay4sms.in/sendsms/"
DLR_URL ="http://pay4sms.in/Dlrcheck/"
token="642910e18bd21e068cc0c669eaf9649a"

msg_status ={"DELIVRD" : True ,"SENT":False, "REJECTD": False}


def send_sms(phone,message,templateid=False):
    credit=2
    sender="VINTNP"
    message=message
    number=phone
    templateid=templateid

    try:
        url=f"{BASE_SMS}?token={token}&credit={credit}&sender={sender}&message={message}&number={number}"
        response = requests.get(url)
        if response.status_code == 200:
            data=response.json()
            msgid = data[0][1]
            check = data[0][2]
            # checkdlrstatus = dlr_status_check(msgid,check)
            # print(checkdlrstatus)
            # return checkdlrstatus
            return True
        
        else:
            return False
    except requests.RequestException as e:
        return False
    

import os
from django.core.files import File
from django.db.models.fields.files import FieldFile

def get_filename(file):    
    filename = ""
    if isinstance(file, (File, FieldFile)):
        filename =  os.path.basename(file.name)
    elif isinstance(file, str):
        filename = os.path.basename(file)
    else :
        filename =None

    return truncate_file_text(filename)



def truncate_text(text,char =10): 
    if not (isinstance(text,str)):
        return text
    if len(text)>10 :
        name = text[0:char]
        return name 
    return text



def truncate_file_text(text,char =10): 
    if not (isinstance(text,str)):
        return text
    if len(text)>10 :
        ext = text.split(".").pop()
        name = text[0:char]
        return name + "." + ext
    return text

# ---------------------------------------


# get pin
def get_pin():
    pin = ''.join([str(random.randint(0, 9)) for _ in range(4)])  
    return pin


# get password
def get_password(name):
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) 
    return password
    

# permissions --------------

import json
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

def load_permissions():
    with open('permission.json', 'r') as file:
        permissions_data = json.load(file)
    return permissions_data

def allow_user(request,klass,instance=False,pk=None):
    allow_msg ='not allowed'
    allow =True    #initial set false

    user=request.user
    role =get_user_role(user)
    if not role:
        return allow ,instance, allow_msg 
    
    model_name= klass.__name__
    action =request.method
    permissions_data = load_permissions()

    company = get_user_company(user)

    if user.is_superuser  :
        return True ,instance, allow_msg  
    
    if model_name in permissions_data['permissions']:
        role_permissions = permissions_data['permissions'][model_name]
        if user.is_authenticated and role in role_permissions:
            allow = role_permissions[role][action]

    
    if pk:
        try :
            instance = klass.objects.get(pk=pk)
            if instance.company in company:
                allow =True
        except:
            instance =False

    return allow ,instance, allow_msg 



def get_user_role(user):

    if user.is_owner and not user.admin:
       return "owner"
    if user.admin:
        return "admin"
    if user.employee:
        return "employee"
    else :
        return False



def get_user(user):
    owner=False
    admin=False
    employee=False

    user_msg =""

    if user.is_owner:
        owner=True
    if user.admin:
        admin=True
    if user.employee:
        employee=True

    return owner,admin,employee

