import json
import logging
from .models import *
from .serializer import *
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseNotFound
from django.utils.dateparse import parse_date
from django.http import JsonResponse, Http404
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination
from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from app.utils import PaginationAndFilter, customPagination,check_user
from django.db import transaction

paginator = PageNumberPagination()

#---------------------------------------------------------------------- Dharshini ----------------------------------------------------------------

#Vendor Registration

@login_required(login_url='login')
def vendor(request):  #change name 
    user=request.user
    allow,msg= check_user(request,VendorRegistration,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)      
    querysets = VendorRegistration.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,VendorRegistration,querysets)    #change, model
    context= {'queryset': queryset,"location":"vendors","pages" :pages,"search":search}   #change location name 
    return render(request,"purchase/vendor.html",context)    #change template name 

@api_view(['POST'])
@login_required(login_url='login')
def add_vendor (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,VendorRegistration,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    request_data=request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id
    serializer = VendorRegistrationSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

@api_view(['PUT'])
@login_required(login_url='login')
def update_vendor(request, pk):  # CHANGE name
    user=request.user
    try:
        instance = VendorRegistration.objects.get(id=pk)  # CHANGE model
    except VendorRegistration.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Category object does not exist'}, status=404)
    allow,msg= check_user(request,VendorRegistration,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = VendorRegistrationSerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['DELETE'])
@login_required(login_url='login')
def delete_vendor(request,pk):
    user=request.user
    try:
        instance = VendorRegistration.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,VendorRegistration,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except VendorRegistration.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    
#Vendor Quatation
#--------------------

@login_required(login_url='login')
def vendorquatation(request):  #change name 
    user=request.user
    allow,msg= check_user(request,VendorQuatation,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    vendors = VendorRegistration.objects.filter(company=request.user.company)  
    querysets = VendorQuatation.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,VendorQuatation,querysets)    #change, model
    context= {'queryset': queryset,"location":"vendorquates","pages" :pages,'vendor_names': vendors,"search":search}   #change location name 
    return render(request,"purchase/vendorquates.html",context)    #change template name
 
@api_view(['POST'])
@login_required(login_url='login')
def add_vendorquatation(request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,VendorQuatation,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    request_data=request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id
    img = request.FILES.get("img",None)
    if user.admin:
        request_data['company'] = user.company.id
    if img:
        request_data['img'] = img
    serializer = VendorQuatationSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
@api_view(['PUT'])
@login_required(login_url='login')
def update_vendorquatation(request, pk):  # CHANGE name
    user=request.user
    try:
        instance = VendorQuatation.objects.get(id=pk)  # CHANGE model
    except VendorQuatation.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Category object does not exist'}, status=404)
    allow,msg= check_user(request,VendorQuatation,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = VendorQuatationSerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@login_required(login_url='login')
def delete_vendorquatation(request,pk):
    user=request.user
    try:
        instance = VendorQuatation.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,VendorQuatation,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except VendorQuatation.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    
#Add Purchases
#--------------------
    
@login_required(login_url='login')
def purchase(request):  #change name 
    user=request.user
    allow,msg= check_user(request,PurchaseInvoice,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    vendors = VendorRegistration.objects.filter(company=request.user.company).order_by("-id")  
    uom =Uom.objects.filter(company=request.user.company).order_by("-id")
    materiallibrary = MaterialLibrary.objects.filter(company=request.user.company).order_by("-id")
    inventory = InventoryStock.objects.filter(company=request.user.company).order_by("-id") 
    querysets = PurchaseInvoice.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,PurchaseInvoice,querysets)    #change, model
    context= {'queryset': queryset,"location":"purchase","pages" :pages,'vendor_names': vendors,"search":search,"uom":uom,
              "inventory":inventory,"materiallibrary":materiallibrary}   #change location name 
    return render(request,"purchase/purchase.html",context)    #change template name


@api_view(['POST'])
@login_required(login_url='login')
def add_purchase(request):
    user = request.user
    allow, msg = check_user(request, PurchaseInvoice, instance=False)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
    invoice_data = request.POST.copy().dict()
    if user.admin:
        invoice_data['company'] = user.company.id
    table = request.data.get('table')  # Use request.data to get JSON data
    invoice_serializer = PurchaseInvoiceSerializer(data=invoice_data)
    if invoice_serializer.is_valid():
        invoice = invoice_serializer.save()
        if table:
            try:
                tdata = json.loads(table)
                for data in tdata:
                    data['invoice'] = invoice.id
                    data['company'] = user.company.id
                    items_serializer = PurchaseItemsSerializer(data=data)
                    if items_serializer.is_valid():
                        items_serializer.save()
                    else:
                        invoice.delete()
                        return JsonResponse(items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except json.JSONDecodeError:
                invoice.delete()
                return JsonResponse({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(invoice_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Purchase List
#--------------------

@login_required(login_url='login')
def purchaselist(request):
    user = request.user
    allow, msg = check_user(request, PurchaseInvoice, instance=False)
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)
    vendors = VendorRegistration.objects.filter(company=request.user.company).order_by("-id")
    querysets = PurchaseInvoice.objects.filter(company=request.user.company).order_by("-id")
    queryset, pages, search = customPagination(request, PurchaseInvoice, querysets)
    context = {'queryset': queryset,"location": "purchaselist","pages": pages,"search": search,'vendor_names': vendors,}
    return render(request, "purchase/purchaselist.html", context)



#Inventory Management
#--------------------

@login_required(login_url='login')
def inventory(request):  #change name 
    user=request.user
    allow,msg= check_user(request,InventoryStock,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    
    querysets = InventoryStock.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,InventoryStock,querysets)    #change, model
    context= {'queryset': queryset,"location":"purchase","pages" :pages,"search":search}   #change location name 
    return render(request,"inventory.html",context)    #change template name

# Quatation
#--------------------

@login_required(login_url='login')
def quatation(request):  #change name 
    user=request.user
    allow,msg= check_user(request,Quatation,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    materiallibrary = MaterialLibrary.objects.filter(company=request.user.company).order_by("-id")  
    uom =Uom.objects.filter(company=request.user.company).order_by("-id")
    site = Project.objects.filter(company=request.user.company).order_by("-id")
    inventory = InventoryStock.objects.filter(company=request.user.company).order_by("-id") 
    querysets = Quatation.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,Quatation,querysets)    #change, model
    context= {"materiallibrary":materiallibrary,'queryset': queryset,"location":"quatation","pages" :pages,"search":search,"uom":uom,"inventory":inventory,'site':site}   #change location name 
    return render(request,"quatation/quatation.html",context)    #change template name

# @api_view(['POST'])
# @login_required(login_url='login')
# def add_quatation(request):
#     user = request.user
#     allow, msg = check_user(request, Quatation, instance=False)
#     if not allow:
#         return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
#     invoice_data = request.POST.copy().dict()
#     if user.admin:
#         invoice_data['company'] = user.company.id
#     if user.employee:
#         invoice_data['created_by'] = user.employee.id
#     print(request.data)
#     table=request.POST.get('table')
#     invoice_serializer = QuatationSerializer(data=invoice_data)
#     if invoice_serializer.is_valid():
#         invoice = invoice_serializer.save()
#         if table:
#             tdata =json.loads(table)
#             for data in tdata:
#                 data['invoice'] = invoice.id
#                 items_serializer = QuatationItemsSerializer(data=data)
#                 if items_serializer.is_valid():
#                     items_serializer.save()
#             return JsonResponse(invoice_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             invoice.delete()
#             return JsonResponse( status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return JsonResponse(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Quatation List

@login_required(login_url='login')
def quatationlist(request):
    user = request.user
    allow, msg = check_user(request, Quatation, instance=False)
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)
    site = Project.objects.filter(company=request.user.company).order_by("-id")
    # quatationitems = QuatationItems.objects.filter(company__name=request.user.company)
    querysets = Quatation.objects.filter(company=request.user.company).order_by("-id")
    queryset, pages, search = customPagination(request, Quatation, querysets)
    context = {'queryset': queryset, "location": "quatationlist", "pages": pages, "search": search, 'site': site}
    return render(request, "quatation/quatationlist.html", context)



# ----------------------------------------------------------------------------------

@login_required(login_url='login')
def transfer(request):  #change name 
    user=request.user
    allow,msg= check_user(request,TransferInvoice,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    uom =Uom.objects.filter(company=request.user.company).order_by("-id")
    site =Project.objects.filter(company=request.user.company).order_by("-id")
    
    from_site = request.GET.get('from',"")
    print(from_site)
    items =[]
    if from_site:
        pro =site.filter(id=from_site).last()
        items = SiteStock.objects.filter(project=pro)
        print(items)
    else:
        items = InventoryStock.objects.filter(company=request.user.company).order_by("-id")

    querysets = TransferInvoice.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,TransferInvoice,querysets)    #change, model
    context= {'queryset': queryset,"location":"transfer","pages" :pages,"search":search,"site":site,"uom":uom,"inventory" :request.user.company,'items' :items}   #change location name 
    return render(request,"transfer/transfer.html",context)    #change template name


from django.db.models import Q
paginator = PageNumberPagination()

@api_view(['GET'])
@login_required(login_url='login')
def transfer_filter(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,Project,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    items =[]
    querysets = TransferInvoice.objects.filter(company=request.user.company).order_by("-id") 
    pk =int(pk)
    if pk == 0:
       querysets =querysets.filter(Q (from_inventory =user.company) | Q (to_inventory=user.company))

    elif pk == -1:
        pass
    else :
        querysets =querysets.filter(Q (from_site__id =pk) | Q (to_site__id = pk))
    # Date Filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        querysets = querysets.filter(created_at__range=[start_date, end_date])
    
    # querysets=querysets.none()
    return PaginationAndFilter(querysets, request, TransferInvoiceSerializer,date_field='created_at')

@api_view(['GET'])
@login_required(login_url='login')
def transfer_from(request,pk):  #change name 
    user=request.user
    allow,msg= check_user(request,Project,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)    
    items =[]

    # try:
    #     instance = TransferInvoice.objects.get(id=pk)  # CHANGE model
    # except TransferInvoice.DoesNotExist:              # CHANGE model
    #     return JsonResponse({'details': ['Item does not exist']}, status=404)

    if pk == 0:
         items = InventoryStock.objects.filter(company=request.user.company).order_by("-id")
         serializers =InventoryStockSerializer (items,many=True)
         return  Response(serializers.data ,status=200)
    else:
        try:
            instance = Project.objects.get(id=pk)  # CHANGE model
            items = SiteStock.objects.filter(project=instance)
            serializers =SiteStockSerializer (items,many=True)
            return  Response(serializers.data ,status=200)
        except Project.DoesNotExist:              # CHANGE model
            return JsonResponse({'details': 'Item does not exist'}, status=404)
    
    


@api_view(['POST'])
@login_required(login_url='login')
def add_transfer(request):
    user = request.user
    allow, msg = check_user(request, TransferInvoice, instance=False)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
    invoice_data = request.POST.copy().dict()
    if user.admin:
        invoice_data['company'] = user.company.id


    source = int(invoice_data.pop('fromsite'))
    destiny = int( invoice_data.pop('tosite') )

    if (source == destiny):
        return JsonResponse ({'tosite': ['From and To Cannot be same site']}, status=400)
    
    if(source == 0) :
        invoice_data ['from_inventory'] = user.company.id
    else :
        invoice_data ['from_site'] = source

    
    if(destiny == 0) :
        invoice_data ['to_inventory'] = user.company.id
    else :
        invoice_data ['to_site'] = destiny


    # print(invoice_data)

    table = invoice_data.pop('table')  # Use request.data to get JSON data
    invoice_serializer = TransferInvoiceSerializer(data=invoice_data)
    if invoice_serializer.is_valid():
        invoice = invoice_serializer.save()
        if table:
            try:
                tdata = json.loads(table)
                for data in tdata:
                    data['invoice'] = invoice.id
                    items_serializer = TransferItemsSerializer(data=data)
                    if items_serializer.is_valid():
                        items_serializer.save()
                    else:
                        invoice.delete()
                        return JsonResponse(items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except json.JSONDecodeError:
                invoice.delete()
                return JsonResponse({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(invoice_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@login_required(login_url='login')
def accept_transfer(request,pk):
    user = request.user
    allow, msg = check_user(request, TransferInvoice, instance=False)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
    invoice_data = request.POST.copy().dict()
    if user.admin:
        invoice_data['company'] = user.company.id

    try:
        instance = TransferInvoice.objects.get(id=pk)  # CHANGE model
    except TransferInvoice.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)

    items = instance.get_transfer_items()
    if not items:
         return JsonResponse({'details': ['Item does not exist']}, status=404)
    
    if items:
        for item in items:
            handle_stock(instance, item)

    instance.item_delivered = True
    instance.received_by = request.user.employee
    instance.save()



def create_site_stock(data):
    return SiteStock.objects.create(**data)

def create_inventory_stock(data):
    return InventoryStock.objects.create(**data)

def update_stock_qty(stock, qty):
    stock.qty -= qty
    stock.save()

def update_destiny_qty(destiny, qty):
    destiny.qty += qty
    destiny.total_supplied_qty += qty
    destiny.save()

def handle_stock(instance, item):
    try:
        if instance.from_site:
            source = instance.from_site.stock
        elif instance.from_inventory:
            source = instance.from_inventory.stock
        else:
            raise ValidationError('Source not specified')

        if instance.to_site:
            destiny = instance.to_site.stock.filter(item=item).last()
            if not destiny:
                destiny = create_site_stock({
                    'project': instance.to_site,
                    'name': item.item,
                    'company': instance.to_site.company,
                })

        elif instance.to_inventory:
            destiny = instance.to_inventory.stock.filter(item=item).last()
            if not destiny:
                destiny = create_inventory_stock({
                    'company': instance.to_site.company,
                    'name': item.item,
                    'unit': source.unit if source else None,  # Assuming source has a unit attribute
                })

        qty = Decimal(item.qty)
        if source and destiny:
            update_stock_qty(source, qty)
            update_destiny_qty(destiny, qty)

    except Exception as e:
        return ValidationError('Item not found')




from django.db.models import F, Value
from django.db.models import Prefetch
from django.db.models.functions import Coalesce

@login_required(login_url='login')
def transferlist(request):
    user = request.user
    allow, msg = check_user(request, TransferInvoice, instance=False)
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)
    site = Project.objects.filter(company=request.user.company).order_by("-id")
    querysets = TransferInvoice.objects.filter(company=request.user.company).order_by("-id")

    queryset, pages, search = customPagination(request, TransferInvoice, querysets)
    context = {'queryset': queryset,"location": "transferlist","pages": pages,"search": search,'site': site,}
    return render(request, "transfer/transferlist.html", context)



@login_required(login_url='login')
def viewstock(request):
    user=request.user
    allow,msg= check_user(request,SiteStock,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)      
    querysets = SiteStock.objects.filter(company=request.user.company).order_by("-id")   #change query
    site =Project.objects.filter(company=request.user.company).order_by("-id")
    
    siteId = request.GET.get('site',None)
    if siteId :
        querysets =querysets.filter(project__id=siteId)
  
    queryset,pages ,search=customPagination(request,Project,querysets)    #change, model
    context= {'queryset': queryset,"location":"viewstock","pages" :pages,"search" :search ,'site' :site ,"selectedSite" :siteId
              
              }   #change location name 
    return render(request,'stock/viewstock.html',context)    #change template name
 

@login_required(login_url='login')
def sitestock(request):
    user=request.user
    allow,msg= check_user(request,SiteStock,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)      
    querysets = SiteStock.objects.filter(project__incharge=user.employee).order_by("-id")   #change query
    site =Project.objects.filter(company=request.user.company).order_by("-id")
    
    print(querysets)
    siteId = request.GET.get('site',None)
    if siteId :
        querysets =querysets.filter(project__id=siteId)
    
    print(querysets)
  
    queryset,pages ,search=customPagination(request,SiteStock,querysets)    #change, model
    context= {'queryset': queryset,"location":"viewstock","pages" :pages,"search" :search ,'site' :site ,"selectedSite" :siteId
              
    }   #change location name 

    return render(request, 'stock/sitestock.html',context)

from decimal import Decimal
@api_view(['POST'])
@login_required(login_url='login')
def site_stock_update(request):
    user=request.user
    allow,msg= check_user(request,SiteStock,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)  

    stock_id =request.POST.get('stock',None)
    qty =request.POST.get('taken_qty',None)
    if not stock_id:
        return JsonResponse({'stock': 'Invalid Stock Item'}, status=404)
    
    try:
        instance = SiteStock.objects.get(id=stock_id)  # CHANGE model
    except SiteStock.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Item does not exist'}, status=404)
    
    qty =Decimal(qty)
    if qty > Decimal(instance.available_qty):
         return JsonResponse({'taken_qty': [f'available quantity exceed for maximum quantity {instance.available_qty}']}, status=400)
    instance.taken_qty =instance.taken_qty + qty
    instance.qty = (instance.qty) - qty
    instance.save()

    inst =DailyMaterialUsage.objects.create(stock = instance,material=instance.item,used =qty,user=request.user)

    return JsonResponse( {'details': ['success']},status=201)       

#Add Project Sub Category
#--------------------
    
@login_required(login_url='login')
def subcontadd(request):  #change name 
    user=request.user
    allow,msg= check_user(request,ProjectSubContract,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)   
    project = Project.objects.filter(company=request.user.company).order_by("-id") 
    type = ContractType.objects.all()
    contractor = Contractor.objects.filter(company=request.user.company).order_by("-id")
    employee = Employee.objects.filter(company=request.user.company).order_by("-id")  
    paymentschedule = PaymentSchedule.objects.all()
    status=WorkStatus.objects.all()
    uom =Uom.objects.filter(company=request.user.company).order_by("-id")
    labourwaves=ProjectSubContractLabourWages.objects.all()
    querysets = ProjectSubContract.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,ProjectSubContract,querysets)    #change, model
    context= {'queryset': queryset,"location":"subcontadd","pages" :pages,"search":search,"uom":uom,
              'paymentschedule':paymentschedule,'employee':employee,'contractor':contractor,'type':type,'project':project,'status':status,
              'labourwaves':labourwaves}   #change location name 
    return render(request,"subcontractor/subcontadd.html",context)    #change template name

#------> Add Project Sub Contractor 

@api_view(['POST'])
@login_required(login_url='login')
def add_subcontadd(request):
    user = request.user
    
    allow, msg = check_user(request, ProjectSubContract, instance=False)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Process contract data
    contract_data = request.POST.copy().dict()
    if user.admin:
        contract_data['company'] = user.company.id
    
    # Extract table data
    table = request.data.get('table')
    
    # Serialize contract data
    contract_serializer = ProjectSubContractSerializer(data=contract_data)
    if contract_serializer.is_valid():
        contract = contract_serializer.save()
        
        # Serialize and save unit rates data
        if table:
            try:
                tdata = json.loads(table)
                for data in tdata:
                    data['contract'] = contract.id
                    items_serializer = ProjectSubContractUnitRatesSerializer(data=data)
                    if items_serializer.is_valid():
                        items_serializer.save()
                    else:
                        contract.delete()
                        return JsonResponse(items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except json.JSONDecodeError:
                contract.delete()
                return JsonResponse({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Automatically create labor wages
        labour_data = {
            'contract': contract.id,
            'maistry': request.data.get('maistry'),
            'maison_cooli': request.data.get('maison_cooli'),
            'male_skilled': request.data.get('male_skilled'),
            'male_unskilled': request.data.get('male_unskilled'),
            'female_skilled': request.data.get('female_skilled'),
            'female_unskilled': request.data.get('female_unskilled'),
        }

        labour_serializer = ProjectSubContractLabourWagesSerializer(data=labour_data)
        if labour_serializer.is_valid():
            labour_serializer.save()
        else:
            contract.delete()
            return JsonResponse(labour_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse(contract_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(contract_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#------> List Project Sub Contractor 
    
@login_required(login_url='login')
def subcontractorlist(request):
    user = request.user
    allow, msg = check_user(request, ProjectSubContract, instance=False)
    if not allow:
        context = {"unauthorized": msg}
        return render(request, "login.html", context)
    project = Project.objects.filter(company=request.user.company).order_by("-id") 
    type = ContractType.objects.all()
    contractor = Contractor.objects.filter(company=request.user.company).order_by("-id")
    employee = Employee.objects.filter(company=request.user.company).order_by("-id")  
    paymentschedule = PaymentSchedule.objects.all()
    status=WorkStatus.objects.all()
    uom =Uom.objects.filter(company=request.user.company).order_by("-id")
    querysets = ProjectSubContract.objects.filter(company=request.user.company).order_by("-id")
    queryset, pages, search = customPagination(request,ProjectSubContract, querysets)
    context = {'queryset': queryset,"location": "subcontractorlist","pages": pages,"search": search,"uom":uom,
        'paymentschedule':paymentschedule,'employee':employee,'contractor':contractor,'type':type,'project':project,'status':status,}
    return render(request, "subcontractor/subcontractorlist.html", context)

#------> Delete Project Sub Contractor 

@api_view(['DELETE'])
@login_required(login_url='login')
def delete_subcontractor(request,pk):
    user=request.user
    try:
        instance = ProjectSubContract.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,ProjectSubContract,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except ProjectSubContract.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)
    
#------> View Project Sub Contractor 

@login_required(login_url='login')
def get_subcontractor(request, pk):
    try:
        subcontractor = ProjectSubContract.objects.get(pk=pk)
        project = Project.objects.filter(company=request.user.company).order_by("-id") 
        type = ContractType.objects.all()
        contractor = Contractor.objects.filter(company=request.user.company).order_by("-id")
        employee = Employee.objects.filter(company=request.user.company).order_by("-id")  
        paymentschedule = PaymentSchedule.objects.all()
        status=WorkStatus.objects.all()
        uom =Uom.objects.filter(company=request.user.company).order_by("-id")

        context = {
            'subcontractor': subcontractor,
            'pk': pk,"uom":uom,
        'paymentschedule':paymentschedule,'employee':employee,'contractor':contractor,'type':type,'project':project,'status':status,
        }

        return render(request, 'subcontractor/subcontractorview.html', context)
    except ProjectSubContract.DoesNotExist:
        return HttpResponseNotFound('<h1>Subcontractor not found</h1>')
    except ValueError:
        return HttpResponseNotFound('<h1>Invalid subcontractor ID</h1>')
    

from rest_framework.response import Response

@api_view(['GET', 'PUT'])
@login_required(login_url='login')
def update_subcontractor(request, pk):
    try:
        subcontractor = ProjectSubContract.objects.get(pk=pk)
    except ProjectSubContract.DoesNotExist:
        return HttpResponseNotFound('<h1>Subcontractor not found</h1>')

    if request.method == 'GET':
        project = Project.objects.filter(company=request.user.company).order_by("-id") 
        type = ContractType.objects.all()
        contractor = Contractor.objects.filter(company=request.user.company).order_by("-id")
        employee = Employee.objects.filter(company=request.user.company).order_by("-id")  
        paymentschedule = PaymentSchedule.objects.all()
        uom = Uom.objects.filter(company=request.user.company).order_by("-id")

        context = {
            'subcontractor': subcontractor,
            'pk': pk,
            'uom': uom,
            'paymentschedule': paymentschedule,
            'employee': employee,
            'contractor': contractor,
            'type': type,
            'project': project, 
        }

        return render(request, 'subcontractor/subcontractorupdate.html', context)

    elif request.method == 'PUT':
       subcontractor_serializer = ProjectSubContractSerializer(subcontractor, data=request.data, partial=True)
    if not subcontractor_serializer.is_valid():
        return Response(subcontractor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    subcontractor_serializer.save()

    table_data = request.data.get('table')
    if table_data:
        try:
            table_data = json.loads(table_data)
            
            ProjectSubContractUnitRates.objects.filter(contract=subcontractor).delete()

            for data in table_data:
                data['contract'] = subcontractor.id
                items_serializer = ProjectSubContractUnitRatesSerializer(data=data)
                if items_serializer.is_valid():
                    items_serializer.save()
                else:
                    return Response(items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)

    wage = subcontractor.get_labour_rates
    labour_data = {
        'maistry': request.data.get('maistry'),
        'maison_cooli': request.data.get('maison_cooli'),
        'male_skilled': request.data.get('male_skilled'),
        'male_unskilled': request.data.get('male_unskilled'),
        'female_skilled': request.data.get('female_skilled'),
        'female_unskilled': request.data.get('female_unskilled'),
    }

    labour_serializer = ProjectSubContractLabourWagesSerializer(wage, data=labour_data)
    if labour_serializer.is_valid():
        labour_serializer.save()
    else:
        return JsonResponse(labour_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(subcontractor_serializer.data)

def update_status(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        new_status_code = request.POST.get('new_status_code')
        
        try:
            project = ProjectSubContract.objects.get(pk=project_id)
            project.status = WorkStatus.objects.get(code=new_status_code)
            project.save()
            return JsonResponse({'success': True})
        except ProjectSubContract.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project not found'})
        except WorkStatus.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid status code'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# ---------------------------------------------------------------------- Azar ---------------------------------------------------------------

# project category

@login_required(login_url='login')
def project_category(request):  #change name 
    user=request.user
    allow,msg= check_user(request,ProjectCategory,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)      
    querysets = ProjectCategory.objects.filter(company=request.user.company).order_by("-id")   #change query
    queryset,pages,search =customPagination(request,ProjectCategory,querysets)    #change, model
    context= {'queryset': queryset,"location":"project-category","pages" :pages,"search" :search,}   #change location name 
    return render(request,"project/procategory.html",context)    #change template name

@api_view(['POST'])
@login_required(login_url='login')
def add_project_category (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,ProjectCategory,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    request_data=request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id

    serializer = ProjectCategorySerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PUT'])
@login_required(login_url='login')
def update_project_category(request, pk):  # CHANGE name
    user=request.user
    try:
        instance = ProjectCategory.objects.get(id=pk)  # CHANGE model
    except ProjectCategory.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Category object does not exist'}, status=404)
    allow,msg= check_user(request,ProjectCategory,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ProjectCategorySerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@login_required(login_url='login')
def delete_project_category(request,pk):
    user=request.user
    try:
        instance = ProjectCategory.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,ProjectCategory,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except ProjectCategory.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)


# material-library
@login_required(login_url='login')
def material_library(request):  #change name 
    user=request.user
    allow,msg= check_user(request,MaterialLibrary,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)      
    querysets = MaterialLibrary.objects.filter(company=request.user.company).order_by("-id")   #change query
    uom =Uom.objects.filter(company=request.user.company).order_by("-id")
    queryset,pages ,search=customPagination(request,MaterialLibrary,querysets)    #change, model
    context= {'queryset': queryset,"location":"material-library","pages" :pages,"search" :search,'uom':uom}   #change location name 
    return render(request,"library/materiallibrary.html",context)    #change template name 

@api_view(['POST'])
@login_required(login_url='login')
def add_material_library (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,MaterialLibrary,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)    
    request_data=request.POST.copy().dict()
    if user.admin:
        request_data['company'] = user.company.id
    serializer = MaterialLibrarySerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@login_required(login_url='login')
def update_material_library(request, pk):  # CHANGE name
    user=request.user
    try:
        instance = MaterialLibrary.objects.get(id=pk)  # CHANGE model
    except MaterialLibrary.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Item does not exist'}, status=404)
    allow,msg= check_user(request,MaterialLibrary,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = MaterialLibrarySerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@login_required(login_url='login')
def delete_material_library(request,pk):
    user=request.user
    try:
        instance = MaterialLibrary.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,MaterialLibrary,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except MaterialLibrary.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)    

# ------------------------------------------------------------------------------------------------


from django.template.loader import render_to_string
# project
@login_required(login_url='login')
def project(request):  #change name 
    user=request.user
    allow,msg= check_user(request,Project,instance=False)  # CHANGE model
    if not allow:
         context ={"unauthorized":msg}
         return render(request,"login.html",context)      
    querysets = Project.objects.filter(company=request.user.company).order_by("-id")   #change query
    category =ProjectCategory.objects.filter(company=request.user.company).order_by("-id")
    engineer =Employee.objects.filter(company=request.user.company).order_by("-id")
    duration =Duration.objects.filter(company=request.user.company).order_by("-id")
    priority =Priority.objects.filter(company=request.user.company).order_by("-id")
    print(category)
    queryset,pages ,search=customPagination(request,Project,querysets)    #change, model
    context= {'queryset': queryset,"location":"project","pages" :pages,"search" :search ,'category' :category ,
        "engineer" :engineer , 'duration' :duration ,"priority" :priority
    }   #change location name 
    return render(request,"project/project.html",context)    #change template name

    html = render_to_string('project/project.html', context)
    return JsonResponse({'html': html})


 
@api_view(['POST'])
@login_required(login_url='login')
def add_project (request):  # CHANGE name
    user=request.user
    allow,msg= check_user(request,Project,instance=False)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)    
    request_data=request.POST.copy().dict()
    modeldesign = request.FILES.get("modeldesign",None)
    aggeaments = request.FILES.get("aggeaments",None) 
    if user.admin:
        request_data['company'] = user.company.id    
    if modeldesign:
         request_data['modeldesign'] = modeldesign    
    if aggeaments: 
         request_data['aggeaments'] = aggeaments 
    serializer = ProjectSerializer(data=request_data)   # CHANGE serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['PUT'])
@login_required(login_url='login')
def update_project(request, pk):  # CHANGE name
    user=request.user
    try:
        instance = Project.objects.get(id=pk)  # CHANGE model
    except Project.DoesNotExist:              # CHANGE model
        return JsonResponse({'details': 'Item does not exist'}, status=404)    
    allow,msg= check_user(request,Project,instance=instance)  # CHANGE model
    if not allow:
        return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = ProjectSerializer(instance, data=request.data,partial=True)   # CHANGE Serializer
    if serializer.is_valid():  
        serializer.save()
        return JsonResponse( serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@login_required(login_url='login')
def delete_project(request,pk):
    user=request.user
    try:
        instance = Project.objects.get(id=pk)  # CHANGE model
        allow,msg= check_user(request,Project,instance=instance)  # CHANGE model
        if not allow:
            return JsonResponse({'details':[msg]}, status=status.HTTP_401_UNAUTHORIZED)
        instance.delete()
        return JsonResponse( {'details': ['success']},status=204)
    except Project.DoesNotExist:  # CHANGE model
        return JsonResponse({'details': ['Item does not exist']}, status=404)

def update_projectstatus(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        new_status_code = request.POST.get('new_status_code')        
        try:
            project = Project.objects.get(pk=project_id)
            project.status = WorkStatus.objects.get(code=new_status_code)
            project.save()
            return JsonResponse({'success': True})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project not found'})
        except WorkStatus.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid status code'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
 
# ---------------------------------------------------------------------------------------------------------




















































































































#------>api
          
#------> api

#------> Dashboard Count

@api_view(['GET'])
@login_required(login_url='apilogin')
def dashboard_count(request):
    user = request.user
    allow, msg = check_user(request, Project, instance=False)
    if not allow:
        return Response({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
    
    today = timezone.now().date()  
    
    project_count = Project.objects.filter(company=user.company).count()
    project_ongoing_count = Project.objects.filter(company=user.company, status__code=1).count()
    project_completed_count = Project.objects.filter(company=user.company, status__code=0).count()

    sub_labour_count = ProjectSubContractLabourAttendence.objects.filter( company=user.company, start_date=today ).count()
    company_labour_count = ProjectLabourAttendence.objects.filter(  company=user.company, date=today ).count()

    material_request_count = Quatation.objects.filter(company=user.company).count()
    
    response_data = {
        'project_count': project_count,
        'project_ongoing_count': project_ongoing_count,
        'project_completed_count': project_completed_count,
        'sub_labour_count': sub_labour_count,
        'company_labour_count': company_labour_count,
        'material_request_count': material_request_count
    }

    return Response(response_data)

#------> Project List 

@api_view(['GET'])
@login_required(login_url='apilogin')
def getprojectlist(request):
    user = request.user
    allow, msg = check_user(request, Project, instance=False)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)

    ONGOING_STATUS_CODE = 1
    COMPLETED_STATUS_CODE = 0


    projects = Project.objects.filter(company=request.user.company).order_by(
        Case(
            When(status__code=ONGOING_STATUS_CODE, then=Value(0)),
            When(status__code=COMPLETED_STATUS_CODE, then=Value(1)),
            output_field=IntegerField(),
        ),
        '-id'
    )
    ongoing_projects = Project.objects.filter(company=user.company, status__code=ONGOING_STATUS_CODE).order_by("-id")
    completed_projects = Project.objects.filter(company=user.company, status__code=COMPLETED_STATUS_CODE).order_by("-id")


    projects = ProjectSerializer(projects, many=True) 
    ongoing_serializer = ProjectSerializer(ongoing_projects, many=True)
    completed_serializer = ProjectSerializer(completed_projects, many=True)

    response_data = {
        'projects':projects.data,
        'ongoing_projects': ongoing_serializer.data,
        'completed_projects': completed_serializer.data
    }

    return Response(response_data)

#-----> Quatation 

@api_view(['GET'])
@login_required(login_url='apilogin')
def getquatation_list(request, pk=None):
    user_company = request.user.company 

    if pk:
        try:
            quatations = Quatation.objects.get(pk=pk, company=user_company)
        except Quatation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = QuatationSerializer(quatations)
        return Response(serializer.data)
    else:
        quatations = Quatation.objects.filter(company=user_company)
        serializer = QuatationSerializer(quatations, many=True)
        return Response(serializer.data)
    


@api_view(['POST'])
@login_required(login_url='apilogin')
@transaction.atomic
def add_quatation(request):
    user = request.user
    allow, msg = check_user(request, Quatation, instance=False)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)
    invoice_data = request.POST.copy().dict()
    if user.admin:
        invoice_data['company'] = user.company.id
    print(request.data)
    table=request.POST.get('table')

    with transaction.atomic():
        invoice_serializer = QuatationSerializer(data=invoice_data)
        if invoice_serializer.is_valid():
            invoice = invoice_serializer.save()
            if table:
                tdata =json.loads(table)
                for data in tdata:
                    data['invoice'] = invoice.id
                    items_serializer = QuatationItemsSerializer(data=data)
                    if items_serializer.is_valid():
                        items_serializer.save()
                    else:
                        invoice.delete()
                        return JsonResponse(items_serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse(invoice_serializer.data, status=status.HTTP_201_CREATED)  
            return JsonResponse({"msg":"error"} ,status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT'])
@login_required(login_url='apilogin')
def update_quatation(request, pk):
    try:
        quatation = Quatation.objects.get(pk=pk)
    except Quatation.DoesNotExist:
        raise Http404

    user = request.user
    allow, msg = check_user(request, Quatation, instance=quatation)
    if not allow:
        return JsonResponse({'details': [msg]}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        serializer = QuatationSerializer(quatation)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        if user.admin:
            data['company'] = user.company.id

        table_data = data.pop('table', [])  # Extract table data

        serializer = QuatationSerializer(quatation, data=data, partial=True)
        if serializer.is_valid():
            updated_quatation = serializer.save()

            # Delete existing QuatationItems associated with the Quatation
            updated_quatation.table.all().delete()

            # Create new QuatationItems based on the updated table data
            for item_data in table_data:
                item_data['invoice'] = updated_quatation.id
                items_serializer = QuatationItemsSerializer(data=item_data)
                if items_serializer.is_valid():
                    items_serializer.save()
                else:
                    return JsonResponse(items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'DELETE'])
def deletequatation(request, pk):
    try:
        # Assuming you want to filter by company associated with the user
        quatation = Quatation.objects.get(pk=pk, company=request.user.company)
    except Quatation.DoesNotExist:
        return Response({'error': 'Quatation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuatationSerializer(quatation)
        return Response({'success': 'Quatation found', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        quatation.delete()
        return Response({'success': 'Quatation deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

#-----> Contract Attendance
    
@api_view(['GET'])
@login_required(login_url='apilogin')
def contractattendance_list(request, pk=None):
    user_company = request.user.company  

    if pk:
        try:
            attendance = ProjectSubContractLabourAttendence.objects.get(pk=pk, company=user_company)
        except ProjectSubContractLabourAttendence.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSubContractLabourAttendenceSerializer(attendance)
        return Response(serializer.data)
    else:
        attendances = ProjectSubContractLabourAttendence.objects.filter(company=user_company)
        serializer = ProjectSubContractLabourAttendenceSerializer(attendances, many=True)
        return Response(serializer.data)

#-----> Labour Attendance

@api_view(['GET'])
@login_required(login_url='apilogin')
def labourattendance_list(request, pk=None):
    user_company = request.user.company 

    if pk:
        try:
            attendance = ProjectLabourAttendence.objects.get(pk=pk, company=user_company)
        except ProjectLabourAttendence.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectLabourAttendenceSerializer(attendance)
        return Response(serializer.data)
    else:
        attendances = ProjectLabourAttendence.objects.filter(company=user_company)
        serializer = ProjectLabourAttendenceSerializer(attendances, many=True)
        return Response(serializer.data)
    
#-----> Expense List

@api_view(['GET'])
@login_required(login_url='apilogin')
def getexpense_list(request, pk=None):
    user_company = request.user.company 

    if pk:
        try:
            expenses = Expense.objects.get(pk=pk, company=user_company)
        except Expense.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(expenses)
        return Response(serializer.data)
    else:
        expenses = Expense.objects.filter(company=user_company)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)


# def profile(request):
#     return render(request, 'profile.html',{})

@api_view(['GET'])
@login_required(login_url='apilogin')
def files_list(request, pk=None):
    user_company = request.user.company

    if pk:
        try:
            files = Files.objects.get(pk=pk, company=user_company)
        except Files.DoesNotExist:
            return Response({'error': 'This id not Valid'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FilesSerializer(files)
        return Response(serializer.data)
    else:
        files = Files.objects.filter(company=user_company)
        if not files.exists():
            return Response({'error': 'No files found for the specified company'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FilesSerializer(files, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
@login_required(login_url='apilogin')
def add_files(request):
    user_company = request.user.company

    files_serializer = FilesSerializer(data=request.data)
    if files_serializer.is_valid():
        files_serializer.save(company=user_company)
        return Response(files_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(files_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT'])
@login_required(login_url='apilogin')
def update_files(request, pk):
    user_company = request.user.company

    try:
        files = Files.objects.get(pk=pk, company=user_company)
    except Files.DoesNotExist:
        return Response({'error': 'Files record not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FilesSerializer(files)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FilesSerializer(files, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Files edited successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@login_required(login_url='apilogin')
def delete_files(request, pk):
    user_company = request.user.company

    if request.method == 'GET':
        try:
            files = Files.objects.get(pk=pk, company=user_company)
        except Files.DoesNotExist:
            return Response({'error': 'Files record not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FilesSerializer(files)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        try:
            files = Files.objects.get(pk=pk, company=user_company)
        except Files.DoesNotExist:
            return Response({'error': 'Files record not found'}, status=status.HTTP_404_NOT_FOUND)

        files.delete()
        return Response({'message': 'File deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@login_required(login_url='login')  
def profile(request):
    user = request.user
    company = user.company if user.admin else None
    company_profile = company.profile.first() if company and company.profile.exists() else None

    user_data = CustomUserSerializer(user).data
    company_data = CompanySerializer(company).data if company else None
    company_profile_data = CompanyProfileSerializer(company_profile).data if company_profile else None

    return render(request, 'profile.html', {
        'user': user_data,
        'company': company_data,
        'company_profile': company_profile_data,
    })

@login_required(login_url='login')
def update_profile(request):
    user = request.user
    company = user.company if user.admin else None

    # Create or retrieve company profile
    if company:
        company_profile, created = CompanyProfile.objects.get_or_create(company=company)
    else:
        company_profile = None

    if request.method == 'POST':
      
        # user.email = request.POST.get('email')
        # user.save()

        if company:
            company.name = request.POST.get('company')
            company.monthly_working_days = request.POST.get('monthly_working_days')
            company.monthly_paid_leaves = request.POST.get('monthly_paid_leaves')
            company.save()

        if company_profile:
            company_profile.email = request.POST.get('email')
            company_profile.phone_number = request.POST.get('phone_number')
            company_profile.gst_number = request.POST.get('gst_number')
            company_profile.address = request.POST.get('address')
            company_profile.area = request.POST.get('area')
            company_profile.save()

        return redirect('profile')  

    user_data = CustomUserSerializer(user).data
    company_data = CompanySerializer(company).data if company else None
    company_profile_data = CompanyProfileSerializer(company_profile).data if company_profile else None

    return render(request, 'update_profile.html', {
        'user': user_data,
        'company': company_data,
        'company_profile': company_profile_data,
    })

@api_view(['GET'])
@login_required(login_url='apilogin')
def machinaryused_list(request, pk=None):
    user_company = request.user.company

    if pk:
        try:
            list = ProjectMachineExpense.objects.get(pk=pk, company=user_company)
        except ProjectMachineExpense.DoesNotExist:
            return Response({'error': 'This id not Valid'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectMachineExpenseSerializer(list)
        return Response(serializer.data)
    else:
        list = ProjectMachineExpense.objects.filter(company=user_company)
        if not list.exists():
            return Response({'error': 'No Machinary Used found for the specified company'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectMachineExpenseSerializer(list, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
@login_required(login_url='apilogin')
def add_machinaryused(request):
    user_company = request.user.company

    list_serializer = ProjectMachineExpenseSerializer(data=request.data)
    if list_serializer.is_valid():
        list_serializer.save(company=user_company)
        return Response(list_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT'])
@login_required(login_url='apilogin')
def update_machinaryused(request, pk):
    user_company = request.user.company

    try:
        list = ProjectMachineExpense.objects.get(pk=pk, company=user_company)
    except ProjectMachineExpense.DoesNotExist:
        return Response({'error': ' Record not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectMachineExpenseSerializer(list)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectMachineExpenseSerializer(list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': ' Machinary Used edited successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@login_required(login_url='apilogin')
def delete_machinaryused(request, pk):
    user_company = request.user.company

    if request.method == 'GET':
        try:
            list = ProjectMachineExpense.objects.get(pk=pk, company=user_company)
        except ProjectMachineExpense.DoesNotExist:
            return Response({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectMachineExpenseSerializer(list)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        try:
            list = ProjectMachineExpense.objects.get(pk=pk, company=user_company)
        except ProjectMachineExpense.DoesNotExist:
            return Response({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        list.delete()
        return Response({'message': ' Machinary Used deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@login_required(login_url='apilogin')
def machinarystock_list(request, pk=None):
    user_company = request.user.company

    if pk:
        try:
            list = DailyMaterialUsage.objects.get(pk=pk, company=user_company)
        except DailyMaterialUsage.DoesNotExist:
            return Response({'error': 'This id not Valid'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DailyMaterialUsageSerializer(list)
        return Response(serializer.data)
    else:
        list = DailyMaterialUsage.objects.filter(company=user_company)
        if not list.exists():
            return Response({'error': 'No Machinary Stock found for the specified company'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DailyMaterialUsageSerializer(list, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
@login_required(login_url='apilogin')
def add_machinarystock(request):
    user_company = request.user.company

    list_serializer = DailyMaterialUsageSerializer(data=request.data)
    if list_serializer.is_valid():
        list_serializer.save(company=user_company)
        return Response(list_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT'])
@login_required(login_url='apilogin')
def update_machinarystock(request, pk):
    user_company = request.user.company

    try:
        list = DailyMaterialUsage.objects.get(pk=pk, company=user_company)
    except DailyMaterialUsage.DoesNotExist:
        return Response({'error': ' Record not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DailyMaterialUsageSerializer(list)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DailyMaterialUsageSerializer(list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': ' Machinary Stock edited successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@login_required(login_url='apilogin')
def delete_machinarystock(request, pk):
    user_company = request.user.company

    if request.method == 'GET':
        try:
            list = DailyMaterialUsage.objects.get(pk=pk, company=user_company)
        except DailyMaterialUsage.DoesNotExist:
            return Response({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DailyMaterialUsageSerializer(list)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        try:
            list = DailyMaterialUsage.objects.get(pk=pk, company=user_company)
        except DailyMaterialUsage.DoesNotExist:
            return Response({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        list.delete()
        return Response({'message': ' Machinary Stock deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def get_employee_profile(request, pk):
    try:
        profile = EmployeeProfile.objects.get(employee_id=pk)
    except EmployeeProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    profile_serializer = EmployeeProfileSerializer(profile)

    data = {
        "employee_id": profile.employee.id,
        "employee_name": profile.employee.name,
        "email": profile.email,
        "mobile": profile.employee.mobile,
        "address": profile.employee.address,
        "image": profile.image.url if profile.image else None,
    }

    return Response(data)

@api_view(['GET'])
def get_project_files(request, project_id):
    try:
        project_files = Files.objects.filter(project_name_id=project_id)
        serializer = FilesSerializer(project_files, many=True)
        return Response(serializer.data)
    except Files.DoesNotExist:
        return Response({'error': 'Files not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_project_expenses(request, project_id):
    try:
        project_expenses = Expense.objects.filter(site_location_id=project_id)
        serializer = ExpenseSerializer(project_expenses, many=True)
        return Response(serializer.data)
    except Expense.DoesNotExist:
        return Response({'error': 'Expenses not found'}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(['GET'])
def get_project_contractorattendance(request, project_id):
    try:
        start_date = request.query_params.get('start_date')

        if not start_date:
            return Response({'error': 'start_date is required'}, status=status.HTTP_400_BAD_REQUEST)

        start_date = parse_date(start_date)

        if not start_date:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        project_contractorattendance = ProjectSubContractLabourAttendence.objects.filter(
            contract_id=project_id,
            start_date=start_date
        )
        
        if not project_contractorattendance.exists():
            return Response({'error': 'Contractor Attendance not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSubContractLabourAttendenceSerializer(project_contractorattendance, many=True)
        return Response(serializer.data)
    except ProjectSubContractLabourAttendence.DoesNotExist:
        return Response({'error': 'Contractor Attendance not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_project_labourattendancefilter(request, project_id):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not start_date or not end_date:
        return Response({'error': 'Both start_date and end_date are required'}, status=status.HTTP_400_BAD_REQUEST)

    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    if not start_date or not end_date:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

    logging.debug(f"Filtering for project {project_id} from {start_date} to {end_date}")

    # Ensure start_date and end_date are inclusive
    project_labourattendance = ProjectLabourAttendence.objects.filter(
        project_id=project_id,
        date__range=(start_date, end_date)
    )

    if not project_labourattendance.exists():
        return Response({'error': 'Labour Attendance not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectLabourAttendenceSerializer(project_labourattendance, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_project_labourattendance(request, project_id):
    try:
        today = timezone.now().date()
        
        project_labourattendance = ProjectLabourAttendence.objects.filter(project_id=project_id, date=today)
        
        if not project_labourattendance.exists():
            return Response({'error': 'Labour Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectLabourAttendenceSerializer(project_labourattendance, many=True)
        return Response(serializer.data)
    except ProjectLabourAttendence.DoesNotExist:
        return Response({'error': 'Labour Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@login_required(login_url='apilogin')
def employee_list(request, pk=None):
    user_company = request.user.company  

    if pk:
        try:
           employee = Employee.objects.get(pk=pk, company=user_company)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    else:
        employee = Employee.objects.filter(company=user_company)
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@login_required(login_url='apilogin')
def inventorymanagement_list(request, pk=None):
    user_company = request.user.company  

    if pk:
        try:
           inventory = InventoryStock.objects.get(pk=pk, company=user_company)
        except InventoryStock.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = InventoryStockSerializer(inventory)
        return Response(serializer.data)
    else:
        inventory = InventoryStock.objects.filter(company=user_company)
        serializer = InventoryStockSerializer(inventory, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@login_required(login_url='apilogin')
def unit_list(request, pk=None):
    user_company = request.user.company  

    if pk:
        try:
           unit = Uom.objects.get(pk=pk, company=user_company)
        except Uom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UomSerializer(unit)
        return Response(serializer.data)
    else:
        unit = Uom.objects.filter(company=user_company)
        serializer = UomSerializer(unit, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
@login_required(login_url='apilogin')
def labour_list(request, pk=None):
    user_company = request.user.company  

    if pk:
        try:
           labour = CompanyLabours.objects.get(pk=pk, company=user_company)
        except CompanyLabours.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CompanyLaboursSerializer(labour)
        return Response(serializer.data)
    else:
        labour  = CompanyLabours.objects.filter(company=user_company)
        serializer = CompanyLaboursSerializer(labour , many=True)
        return Response(serializer.data)


@api_view(['GET'])
def project_site_location_filter(request):
    projects = Project.objects.values('id', 'proj_name', 'site_location')
    site_locations = [{'id': project['id'], 'name': project['proj_name'], 'site_location': project['site_location']} for project in projects]
    return Response(site_locations)

@api_view(['GET'])
def payment_schedule_list(request, pk=None):
    if pk:
        try:
            payment_schedule = PaymentSchedule.objects.get(pk=pk)
        except PaymentSchedule.DoesNotExist:
            return Response({'error': 'Payment schedule not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentScheduleSerializer(payment_schedule)
        return Response(serializer.data)
    else:
        payment_schedules = PaymentSchedule.objects.all()
        serializer = PaymentScheduleSerializer(payment_schedules, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@login_required(login_url='apilogin')
def machine_list(request, pk=None):
    user_company = request.user.company  

    if pk:
        try:
           machine = CompanyMachinaryCharges.objects.get(pk=pk, company=user_company)
        except CompanyMachinaryCharges.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CompanyMachinaryChargesSerializer(machine)
        return Response(serializer.data)
    else:
        machine  = CompanyMachinaryCharges.objects.filter(company=user_company)
        serializer = CompanyMachinaryChargesSerializer(machine , many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def get_project_machinaryused(request, project_id):
    try:
        project_machinaryused = ProjectMachineExpense.objects.filter(project_id=project_id)
        serializer = ProjectMachineExpenseSerializer(project_machinaryused, many=True)
        return Response(serializer.data)
    except ProjectMachineExpense.DoesNotExist:
        return Response({'error': 'Machinary Used not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@login_required(login_url='apilogin')
def materiallibrary_list(request, pk=None):
    user_company = request.user.company  
    if pk:
        try:
           material_library = MaterialLibrary.objects.get(pk=pk, company=user_company)
        except MaterialLibrary.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MaterialLibrarySerializer(material_library)
        return Response(serializer.data)
    else:
        material_library  = MaterialLibrary.objects.filter(company=user_company)
        serializer = MaterialLibrarySerializer(material_library, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
@login_required(login_url='apilogin')
def sitestock_list(request, pk=None):
    user_company = request.user.company  
    if pk:
        try:
           sitestock_list = SiteStock.objects.get(pk=pk, company=user_company)
        except SiteStock.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SiteStockSerializer(sitestock_list)
        return Response(serializer.data)
    else:
        sitestock_list  = SiteStock.objects.filter(company=user_company)
        serializer = SiteStockSerializer(sitestock_list, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def user_list(request):
    user = CustomUser.objects.values('id', 'name')
    users = [{'id': user['id'], 'name': user['name']} for user in user]
    return Response(users)

@api_view(['GET'])
def contractoratt_list(request):
    contractor = Contractor.objects.values('id', 'name')
    contractors = [{'id': contractor['id'], 'name': contractor['name']} for contractor in contractor]
    return Response(contractors)

@api_view(['GET'])
def sub_contract_list(request):
    sub_contract = ProjectSubContract.objects.values('id', 'name', )
    sub_contracts = [{'id': sub_contract['id'], 'name': sub_contract['name']} for sub_contract in sub_contract]
    return Response(sub_contracts)