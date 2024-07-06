from django.urls import path
from.import views
from app import api
from django.contrib import admin
from django.conf import settings
#from .views import attendancelist
from .views import CustomLogoutView
from django.urls import reverse_lazy
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_view

from django.shortcuts import render
from django.conf.urls import handler404

# def custom_404(request, exception):
#     return render(request, 'errors/404.html', status=404)


# # views.py
# from django.http import HttpResponse

# def trigger_error(request):
#     division_by_zero = 1 / 0  
#     return HttpResponse("This won't be reached")


# def custom_500(request):
#     return render(request, 'errors/500.html', status=500)

# handler404 = custom_404
# handler500 = custom_500



urlpatterns = [

#----------------------------------------------------------- Dharshini --------------------------------------------------------------------------

    path('login/', views.login_admin, name='login'), 
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),

#---------------------------- UOM ----------------------------

    path('uom/', views.uom, name='uom'),
    path('add-uom/', views.add_uom, name='add-uom'),
    path('update-uom/<int:pk>/', views.update_uom, name='update-uom'),
    path('delete-uom/<int:pk>/', views.delete_uom, name='delete-uom'),

    # path('uom/', views.uom, name='uom') ,            
    # path('get_data/<int:id>/', views.get_data, name='get_data'),
    # path('delete_uom/<int:id>/', views.delete_uom, name='delete_uom'),
    # path('save_data/<int:id>/', views.save_data, name='save_data'),

#------------------------ Company Staff --------------------

    path('process-status', views.get_process_status, name='process-status'),

#---- Employee Role ----

    path('emproles/',views.emproles, name="emproles"),           
    path('add_emproles/',views.add_emproles, name="add-emproles"), 
    path('update_emproles/<int:id>/',views.update_emproles, name="update-emproles"), 
    path('get_emproles/<int:id>/', views.get_emproles, name='get_emproles'),
    path('delete_emproles/<int:id>/', views.delete_emproles, name='delete_emproles'),
    # path('save_emproles/<int:id>/', views.save_emproles, name='save_emproles'),

#---- Employee ----

    path('employee/',views.employee,name= 'employee'),          
    path('get_employee/<int:id>/', views.get_employee, name='get_employee'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('save_employee/<int:id>/', views.save_employee, name='save_employee'),

#-------------------------- Purchases --------------------

#----- Vendor Registration -----

    path('vendor/', api.vendor, name='vendors'),
    path('vendor-list/', api.vendor_list, name='vendors-list'),
    path('add_vendor/', api.add_vendor, name='add_vendor'),
    path('update_vendor/<int:pk>/', api.update_vendor, name='update_vendor'),
    path('delete_vendor/<int:pk>/', api.delete_vendor, name='delete_vendor'),

#----- Vendor Quatation -----

    path('vendorquatation/', api.vendorquatation, name='vendorquates'),
    path('add_vendorquatation/', api.add_vendorquatation, name='add_vendorquatation'),
    path('update_vendorquatation/<int:pk>/', api.update_vendorquatation, name='update_vendorquatation'),
    path('delete_vendorquatation/<int:pk>/', api.delete_vendorquatation, name='delete_vendorquatation'),

#----- Add Purchase -----

    path('purchase/',api.purchase, name="purchase"),
    path('purchase-list/<str:pk>/',views.purchase_list, name="purchase-ist"),
    path('add_purchase/', api.add_purchase, name='add_purchase'),

#----- Purchase List -----

    path('purchaselist/',api.purchaselist,name='purchaselist'), 

    path('project-purchase-history/<int:pk>/',api.project_purchaselist,name='project-purchase-history'),
    path("purchase-status-change/<int:pk>/",api.purchase_status_change, name = 'purchase-status-change') ,
    # path('purchase-filter/<str:pk>/', api.purchase_filter, name="purchase_filter"),

#-------------------------- Quatation --------------------

# #----- Add Quatation -----

#     path('quatation/',api.quatation, name="quatation"),
#     path('add_quatation/',api.add_quatation, name='add_quatation'),

# #----- Quatation List -----

#     path('quatation-payment/<str:pk>/', api.quatation_payment, name="quatation-payment"),
#     path('quatation-payment-date/<int:pk>/', api.quatation_payment_date, name="quatation-payment_date"),

#------------------- Inventory Management ----------------

    path('inventory/',api.inventory, name="inventory"), 

#----------------------- Transfer Item --------------------

    path('transfer/',api.transfer, name="transfer"),
    path('transfer/<int:pk>/',api.transfer_from, name="transfer"),
    path('add_transfer/',api.add_transfer, name='add_transfer'),
    path('accept_transfer/',api.accept_transfer, name='accept_transfer'),
    path('transferlist/', api.transferlist, name="transferlist"),
    path('transfer-filter/<str:pk>/', api.transfer_filter, name="transfer_filter"),  


    path('quotation/add/',api.quatation, name="quatation"),  
    path('quatation-list/<str:pk>/',views.quatation_list, name="quatation-ist"),  
    path('add_quatation/',api.add_quatation, name='add_quatation'),   
    path('quotation/', api.quatationlist, name="quatationlist"),
    path("quatation-status-change/<int:pk>/",api.quatation_status_change, name = 'quatation-status-change') ,
    path('update_quotation_status/', api.update_quotation_status_api, name='update_quotation_status'),
  
#----------------------- Site Stocks ----------------------

    path('sitestock/',api.sitestock, name="sitestock"),
    path('update-site-stock' ,api.site_stock_update,name='site-stock-update'),

    path('viewstock/',api.viewstock, name="viewstock"),
 
#------------------------- Sub Contractor List --------------------

    path('subcontadd/',api.subcontadd, name="subcontadd"),
    path('add_subcontadd/', api.add_subcontadd, name='add_subcontadd'),
    path('subcontractorlist/',api.subcontractorlist, name="subcontractorlist"),
    path('subcontractorview/<int:pk>/', api.get_subcontractor, name='subcontractorview'),
    path('update_subcontractor/<int:pk>/', api.update_subcontractor, name='update_subcontractor'),
    path('delete_subcontractor/<int:pk>/', api.delete_subcontractor, name='delete_subcontractor'),
    path('update_status/', api.update_status, name='update_status'),
#---------------------------------------------------------------------- End Dharshini ------------------------------------------------------------------

#------------------------------------------------------------------------- Azar -----------------------------------------------------------------------

#----------- material library ---------------------------

    path('material-library/', api.material_library, name='material-library'),
    # api
    path('add_material-library/', api.add_material_library, name='add_material-library'),
    path('update_material-library/<int:pk>/', api.update_material_library, name='update_material-library'),
    path('material-library/<int:pk>/', api.delete_material_library, name='material-library'),


    #---------------------------------------------------- category ------------------------------------------------------------

    path('contract-category/', views.contract_category, name='contractcategory'),
    path('add-contract-category/', views.add_contract_category, name='add-contract-category'),
    path('update-contract-category/<int:pk>/', views.update_contract_category, name='update-contract-category'),
    path('contract-category/<int:pk>/', views.delete_contract_category, name='delete-contract-category'),

#----------------------------------------------------Contractor-------------------------------------------------------------

    path('contractor/', views.contractor, name='contractor'),
    path('add-contractor/', views.add_contractor, name='add-contractor'),
    path('update-contractor/<int:pk>/', views.update_contractor, name='update-contractor'),
    path('delete-contractor/<int:pk>/', views.delete_contractor, name='delete-contractor'),

    # project category  
    # render
    path('project-category/', api.project_category, name='project-category'), 
  
    # api
    path('add_project-category/', api.add_project_category, name='add_project-category'),
    path('update_project-category/<int:pk>/', api.update_project_category, name='update_project-category'),
    path('delete_project-category/<int:pk>/', api.delete_project_category, name='delete_project-category'),

    # project
    path('project/', api.project, name='project'), 
    path('project/<str:filter_by>/', api.project, name='project_filtered'), 


    # api
    path('add_project/', api.add_project, name='add_project'), 
    path('update_project/<int:pk>/', api.update_project, name='update_project'),
    path('delete_project/<int:id>/', api.delete_project, name='delete_project'),
    path('enable_project/<int:id>/', api.enable_project, name='enable_project'),
    # path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('update_projectstatus/', api.update_projectstatus, name='update_projectstatus'),

    path('attendance/subcontract',views.attendancereport,name= 'proattendance'),
    path('add_attendance/', views.add_attendancereport, name='add_attendance'),
    path('update_attendancereport/<int:pk>/', views.update_attendancereport, name='update_attendancereport'),
    path('delete_attendancereport/<int:pk>/', views.delete_attendancereport, name='delete_attendancereport'),
    # path('attendancelist/<int:pk>/', views.attendancelist, name='attendancelist'),
    path('attendancelist/<str:pk>/', views.attendancelist, name="attendancelist"),
    path('attendancelists/<str:pk>/', views.attendancelistpro, name="attendancelist"),

    # path('contractcategory/',views.contractcategory,name= 'contractcategory'),
    path('contractor',views.contractor,name= 'contractor'), 
     
    path('invoice/',views.invoice, name="invoice"),   
    path('payment/',views.payment, name="payment"),    
    path('permission/',views.permission, name="permission"),
    # path('procategory/',views.procategory, name="procategory"),
    # path('edit_category/<int:category_id>/', views.procategory, name='edit_category'),
    path('profit/',views.profit, name="profit"),   
    path('projectlist/',views.projectlist,name='projectlist'),  

# --------------------------------------------------------  *****  SALARY  ******** ---------------------------------------------

    path('labour-salary-list/<str:pk>/',views.labour_salary_list,name="labour-salary-list"),
    path('labour-salary/',views.labour_salary,name='labour-salary'),
    path('make-labour-salary/<int:pk>/',views.make_labour_salary,name='make-labour-salary'),
    path('make-labour-payment/<int:pk>/',views.make_labour_payment,name="labour-payment"),

    path("employee_salary_list/<str:pk>/" , views.employee_salary_list,name="emp-salary-list"),
    path('employee-salary/<int:pk>/',views.employee_labour_salary, name="employee_labour_salary"),
    path('employee-salary/',views.employee_salary, name="employee-salary"),

    path('contractor-payment/',views.contractor_payment_management, name="contractor-payment"),
    path('signin/',views.signin, name="SignIn"),            
   
#-----------------------------------------------------Expense------------------------------------------------------------

    path('expense/', views.expense, name='expense'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('update_expense/<int:pk>/', views.update_expense, name='update_expense'),
    path('delete_expense/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('expenselist/',views.expense_list,name='expense_list'),
    path('expense_list/<int:pk>/', views.expenselist, name='expenselist'),

#----------------------------------------------Machinary Charges----------------------------------------------------------

    path('machinary_charges/', views.machinary_charges, name='machinary_charges'),
    path('add_machinary_charges/', views.add_machinary_charges, name='add_machinary_charges'),
    path('update_machinary_charges/<int:pk>/',views.update_machinary_charges, name='update_machinary_charges'),
    path('delete_machinary_charges/<int:pk>/',views.delete_machinary_charges, name='delete_machinary_charges'),

#-------------------------------------labourroles and salary--------------------------------------------------------

    path('labour_roles_and_salary/', views.labour_roles_and_salary, name='labour_roles_and_salary'),
    path('add_labour_role/', views.add_labour_roles_and_salary, name='add_labour_role'),
    path('update_labour_role/<int:pk>/', views.update_labour_roles_and_salary, name='update_labour_role'),
    path('delete_labour_role/<int:pk>/', views.delete_labour_roles_and_salary, name='delete_labour_role'),

#---------------------------------------------- Labours -------------------------------------------------------------

    path('labours/',views.labours, name='labours'),
    path('add_labours/',views.add_labours, name='add_labours'),
    path('update_labours/<int:pk>/',views.update_labours, name='update_labours'),
    path('delete_labours/<int:pk>/',views.delete_labours, name='delete_labours'),



    # contractor payment

    # path('pending/',views.pending, name="pending"),
    path('contractor-payment/<str:pk>/', views.contractor_payment, name="contractor-payment"),
    path('contractor-payment-date/<int:pk>/', views.contractor_payment_date, name="contractor-payment_date"),

    path('make-contract-payment/<int:pk>/',views.make_contract_payment,name="subcontract-payment"),

    #  payment history
    path('make-invoice-payment/<int:pk>/',views.make_invoice_payment,name="make_invoice_payment"),

    path('signin/',views.signin, name="SignIn"),  


    # #-------------------------------------------------- City ------------------------------------------

    # path('city/',views.city,name= 'city'),
    # path('addcity/',views.addcity,name= 'addcity'),
    # path('updatecity/<str:id>',views.updatecity,name='updatecity'),
    # path('deletecity/<str:id>',views.deletecity,name='deletecity'),

# #-------------------------------------------------- Country ---------------------------------------

#     path('country/',views.country,name= 'country'),
#     path('addcountry/',views.addcountry,name= 'addcountry'),
#     path('updatecountry/<str:id>',views.updatecountry,name='updatecountry'),
#     path('deletecountry/<str:id>',views.deletecountry,name='deletecountry'),

# #-------------------------------------------------- District --------------------------------------

#     path('district/',views.district,name= 'district'),
#     path('adddistrict/',views.adddistrict,name= 'adddistrict'),
#     path('updatedistrict/<str:id>',views.updatedistrict,name='updatedistrict'),
#     path('deletedistrict/<str:id>',views.deletedistrict,name='deletedistrict'),

# #---------------------------------------------------- Role ----------------------------------------

#     path('roles/',views.roles, name="roles"), 
#     path('addroles/',views.addroles,name= 'addroles'),
#     path('updateroles/<str:id>',views.updateroles,name='updateroles'),
#     path('deleteroles/<str:id>',views.deleteroles,name='deleteroles'),

    #path('api/counts/', views.count_api, name='counts-api'),

    # --------------------------------------- Attendence ------------------------------------------------------------------

    
    # labour attendence
    path('attendance/labour',views.companylabour_attendance,name= 'company-labour-attendance'),
    path('company-labour-attendance/add/', views.add_companylabourattendance, name='add_companylabourattendance'),
    path('update_companylabourattendance/<int:pk>/', views.update_companylabourattendance, name='update_companylabourattendance'),
    path('delete_companylabourattendance/<int:pk>/', views.delete_companylabourattendance, name='delete_companylabourattendance'),
    # path('attendancelist/<int:pk>/', views.attendancelist, name='attendancelist'),
    path('companylabourattendancelist/<str:pk>/', views.companylabourattendancelist, name="companylabourattendancelist"),

    path('labour-attendence-list/<str:pk>/',views.labour_attendence_list,name='labour-attendence-list'),
    path('make-present/<int:pk>/',views.make_labour_present,name='make_labour_present'),



    # employee attendence
    path('attendance/employee',views.employee_attendance,name= 'employee-labour-attendance'), #render only
    path('add_employeeattendance/', views.add_employeeattendance, name='add_employeelabourattendance'),
    path('employee_companylabourattendance/<int:pk>/', views.update_employeeattendance, name='update_employeeabourattendance'),
    path('employee_companylabourattendance/<int:pk>/', views.delete_employeeattendance, name='delete_employeelabourattendance'),
    path('employeelabourattendancelist/<str:pk>/', views.employeeattendancelist, name="employeelabourattendancelist"),

    path('employee-attendence-list/<str:pk>/',views.employee_attendence_list,name='labour-attendence-list'), #list data
    path('make-employee-present/<int:pk>/',views.make_employee_present,name='make_employee_present'),



    path('employee-clockin',views.employee_clock_in,name ='employe-clockin'),
    path('employee-clockout/<int:pk>/',views.employee_clock_out,name = 'employe-clockout'),

# --------

# ACCOUNTS ---------------------------------

    path('profit-loss/<str:pk>/',views.profit_and_loss,name="profit-and-loss"),
    path('pettycash/', views.pettycash, name='pettycash'),
    path('pettycash_list/', views.pettycash_list, name='pettycash_list'),
    path('pettycash_list/<int:pk>/', views.pettycash_list, name='pettycash_detail'),
    path('add_pettycash/', views.add_pettycash, name='add_pettycash'),
    path('update_pettycash/<int:pk>/', views.update_pettycash, name='update_pettycash'),
    path('delete_pettycash/<int:pk>/', views.delete_pettycash, name='delete_pettycash'),

    path('clientcash/<int:pk>/',views.clientcash,name='clientcash'),
    path('clientcashpay/<int:pk>/', views.clientcashpay, name='clientcashpay'),
    path('update_clientcashpay/<int:payment_id>/', views.update_clientcashpay, name='update_clientcashpay'),

    path('project_schedule/<int:pk>/',views.project_schedule,name='project_schedule'),
    path('add_project_schedule/<int:pk>/', views.add_project_schedule, name='add_project_schedule'),
    path('delete-project-schedule/<int:pk>/', views.delete_project_schedule, name='delete-project-schedule'),
    path('update-project-schedule/<int:pk>/', views.update_project_schedule, name='update-project-schedule'),
    path('update-project-schedule-status/', views.update_project_schedule_status, name='update_project_schedule_status'),
    # path('project_schedule_history/<int:pk>/', views.project_schedule_history, name='project_schedule_history'),





    # path('project-schedulehistory/<int:pk>/', views.project_schedulehistory, name='project_schedulehistory'),
    path('project-schedulehistory/<int:pk>/', views.project_schedulehistory, name='project_schedulehistory'),
    path('add-project-schedulehistory/<int:pk>/', views.add_project_schedulehistory, name='add_project_schedulehistory'),  # Add this line
    path('delete-project-schedule-history/<int:pk>/', views.delete_project_schedule_history, name='delete-project-schedule-history'),
    path('update-project-schedule-history/<int:pk>/', views.update_project_schedule_history, name='update-project-schedule-history'),
    # path('api/share-project-schedule-history/<int:project_id>/', views.share_project_schedule_history, name='share_project_schedule_history'),
    # path('api/share-project-schedule-history/', views.share_project_schedule_history, name='share_project_schedule_history'),


    path('send-whatsapp/<int:pk>/', views.send_whatsapp_message, name='send_whatsapp_message'),
 
    #     # employee attendence
    # path('attendance/employee',views.employee_attendance,name= 'employee-labour-attendance'), #render only
    # path('add_employeeattendance', views.add_employeeattendance, name='add_employeelabourattendance'),
    # path('employee_companylabourattendance/<int:pk>/', views.update_employeeattendance, name='update_employeeabourattendance'),
    # path('employee_companylabourattendance/<int:pk>/', views.delete_employeeattendance, name='delete_employeelabourattendance'),
    # path('employeelabourattendancelist/<str:pk>/', views.employeeattendancelist, name="employeelabourattendancelist"),

    # path('employee-attendence-list/<str:pk>/',views.employee_attendence_list,name='labour-attendence-list'), #list data
    # path('make-employee-present/<int:pk>/',views.make_employee_present,name='make_employee_present'),

    path('site_allocation/',views.site_allocation,name= 'site_allocation'), 
    path('add_site_allocation/', views.add_site_allocation, name='add_site_allocation'),
    path('site-allocation-list/<str:pk>/',views.site_allocation_list,name='site-allocation-list'), #list data
    path('site_allocationemployee/<int:pk>/', views.site_allocationemployee, name='site_allocationemployee'),

    path('site_allocationlabour/<int:pk>/', views.site_allocationlabour, name='site_allocationlabour'),



    path('delete_site_allocation_list/<int:pk>/', views.delete_site_allocation_list, name='delete_site_allocation_list'),


    path('lab_site_allocation/',views.lab_site_allocation,name= 'lab_site_allocation'), 
    path('add_lab_site_allocation/', views.add_lab_site_allocation, name='add_lab_site_allocation'),
    path('lab-site-allocation-list/<str:pk>/',views.lab_site_allocation_list,name='lab-site-allocation-list'), 


    path('purchase-details/<int:purchase_id>/', views.purchase_details, name='purchase-details'),
    #path('update-purchase/<int:purchase_id>/',  views.purchase_details, name='update_purchase_details'),
    path('purchase_update/<int:pk>/', views.update_purchase, name='update_purchase'),
    path('purchase_details/<int:pk>/', views.get_purchase, name='purchase_details'),

    path('purchasetableupdate/<str:id>/', views.purchasetableupdate, name='purchasetableupdate'),

    # path('purchaseitems/<int:pk>/', views.update_purchase_item, name='update_purchase_item'),

    path('quatation_update/<int:pk>/', views.update_quatation, name='update_quatation'),
    path('quatationtableupdate/<str:id>/', views.quatationtableupdate, name='quatationtableupdate'),
    path('quatation_details/<int:pk>/', views.get_quatation, name='quatation_details'),



    


# revision

    path('purchase-track/<int:pk>/<int:site_or_inventory>/' , views.item_price_track,name="item_price_track"),





        
















  #-------------------------------> Mobile Team API

    path('register/', views.registration_view, name='register'),
    path('apilogin/', views.login_view, name='api-login'),
    path('reset_pin/', views.reset_pin, name='reset_pin'), 
    path('generate_otp/', views.generate_otp, name='generate_otp'),  #generate otp for pin reset
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_confirm/', views.reset_confirm, name='reset_confirm'),  # mpin reset url
    path('login_with_token_and_pin/', views.login_with_token_and_pin, name='login_with_token_and_pin'),

    path('dashboard-count/', api.dashboard_count, name='dashboard-count'),
    path('project-list/', api.getprojectlist, name='project-list'),

    # path('quatation-list/', api.getquatation_list, name='quatation-list'),  
    path('quatation/<int:pk>/', api.getquatation_list, name='get_quatation_detail'),
    path('delete-quatation/<int:pk>/', api.deletequatation, name='delete-quatation'),
    path('update_quatation/<int:pk>/', api.update_quatation, name='update_quatation'),

    path('delete-quatationitem/<int:pk>/', api.deletequatationitem, name='delete-quatation'),
    path('update_quatationitem/<int:pk>/', api.update_quatationitem, name='update_quatation'),
    
    path('contractattendance-list/', api.contractattendance_list, name='contractattendance-list'),
    path('contractattendance-list/<int:pk>/',  api.contractattendance_list, name='contractattendance-detail'),

    path('labourattendance-list/', api.labourattendance_list, name='labourattendance-list'),
    path('labourattendance-list/<int:pk>/',  api.labourattendance_list, name='labourattendance-detail'),

    path('getexpense-list/', api.getexpense_list, name='getexpense-list'),
    path('getexpense-list/<int:pk>/',  api.getexpense_list, name='getexpense-detail'),

    path('profile/', api.profile, name='profile'),
    path('profile/update/', api.update_profile, name='update_profile'),

    path('files-list/', api.files_list, name='files-list'),
    path('files-list/<int:pk>/',  api.files_list, name='files-detail'),
    path('add_files/', api.add_files, name='add_files'),
    path('update_files/<int:pk>/', api.update_files, name='update_files'),
    path('delete_files/<int:pk>/', api.delete_files, name='delete_files'),

# -------------------- dailytask --------------------------------------

    path('dailytask/', views.dailytask, name='dailytask'),  
    path('add_dailytask/', views.add_dailytask, name='add_dailytask'),  
    path('update_dailytask/<int:pk>/', views.update_dailytask, name='update_dailytask'), 
    # path('delete_dailytask/<int:pk>/', views.delete_dailytask, name='delete_dailytask'),  
    # path('dailytask-list/', views.dailytask_list, name='dailytask-list'),
    path('dailytask-list/<int:project_id>/',  views.dailytask_list, name='dailytask-detail'),
    path('delete_dailytask/<int:pk>/', views.delete_dailytask, name='delete_dailytask'), 

# ------------------ sitestockusage  --------------

    path('dailysitestockusage/', api.dailysitestockusage, name='dailysitestockusage'), 
    path('add_dailysitestockusage/',api.add_dailysitestockusage, name='add_dailysitestockusage'),
    path('stockusagelist/', api.sitestockusage, name="dailysitestockusagelist"),
    path('update-stock-status/', api.update_stock_status, name='update_stock_status'),
    path('dailysitestockusagelist/<int:pk>/', api.dailysitestockusagelist, name='dailysitestock-usagelist'), 
    # path("usage_status_change/<int:pk>/",api.usage_status_change, name = 'usage_status_change') ,

    # path('dailysitestockusage/', api.dailysitestockusage, name='dailysitestockusage'),

    path('save_data/<int:pk>/', api.save_data, name='save_data'),

    path('update_sitestockusage/<int:pk>/', api.update_sitestockusage, name='update_sitestockusage'), 
    path('delete_sitestockusage/<int:pk>/', api.delete_sitestockusage, name='delete_sitestockusage'),


# -----------------------------------------------------------------


    path('machinaryused-list/', api.machinaryused_list, name='machinaryused-list'),
    path('machinaryused-list/<int:pk>/',  api.machinaryused_list, name='machinaryused-detail'),
    path('add_machinaryused/', api.add_machinaryused, name='add_machinaryused'),
    path('update_machinaryused/<int:pk>/', api.update_machinaryused, name='update_machinaryused'),
    path('delete_machinaryused/<int:pk>/', api.delete_machinaryused, name='delete_machinaryused'),

    path('machinarystock-list/', api.machinarystock_list, name='machinarystock-list'),
    path('machinarystock-list/<int:pk>/',  api.machinarystock_list, name='machinarystock-detail'),
    path('add_machinarystock/', api.add_machinarystock, name='add_machinarystock'),
    path('update_machinarystock/<int:pk>/', api.update_machinarystock, name='update_machinarystock'),
    path('delete_machinarystock/<int:pk>/', api.delete_machinarystock, name='delete_machinarystock'),


    path('project-files/<int:project_id>/', api.get_project_files , name='project-files'),
    path('project-expenses/<int:project_id>/', api.get_project_expenses , name='project-expenses'),
    path('project-contractorattendance/<int:project_id>/', api.get_project_contractorattendance , name='project-contractorattendance'),
    path('project-labourattendance/<int:project_id>/', api.get_project_labourattendance , name='project-labourattendance'),
    path('project-labourattendancefilter/<int:project_id>/', api.get_project_labourattendancefilter , name='project-labourattendancefilter'),
    path('project-machinaryused/<int:project_id>/', api.get_project_machinaryused , name='project-machinaryused'),


    path('employee-list/', api.employee_list, name='employee-list'),
    path('employee-list/<int:pk>/',  api.employee_list, name='employee-detail'),

    path('inventory-list/', api.inventorymanagement_list, name='inventory-list'),
    path('inventory-list/<int:pk>/',  api.inventorymanagement_list, name='inventory-detail'),

    path('unit-list/', api.unit_list, name='unit-list'),
    path('unit-list/<int:pk>/',  api.unit_list, name='unit-detail'),

    path('labour-list/',  api.labour_list, name='labour-list'),
    path('labour-list/<int:pk>/',  api.labour_list, name='labour-detail'),

    path('site_location_filter/', api.project_site_location_filter, name='site_location_filter'),

    path('payment-schedule-list/',  api.payment_schedule_list, name='payment-schedule-list'),
    path('payment-schedule-list/<int:pk>/',  api.payment_schedule_list, name='payment-schedule-detail'),

    path('machine-list/',  api.machine_list, name='machine-list'),
    path('machine-list/<int:pk>/',  api.machine_list, name='machine-detail'),

    path('materiallibrary-list/',  api.materiallibrary_list, name='materiallibrary-list'),
    path('materiallibrary-list/<int:pk>/',  api.materiallibrary_list, name='materiallibrary-list'),

    path('sitestock-list/',  api.sitestock_list, name='sitestock-list'),
    path('sitestock-list/<int:pk>/',  api.sitestock_list, name='sitestock-list'),

    path('user-list/', api.user_list, name='user-list'),
    path('contractor-list/', api.contractoratt_list, name='contractor-list'),
    # path('sub-contract-list/', api.sub_contract_list, name='sub-contract-list'),
    path('sub-contract-list/<int:project_id>/', api.get_sub_contract_lists , name='get_sub_contract_lists'),
    # path('sub-contract-list/<int:pk>/', api.sub_contract_list, name='sub-contract-list'),

   
    path('employee-profile/<int:pk>/', api.get_employee_profile, name='get-employee-profile'),



    path('dailysitestockusage/', api.dailysitestockusage, name='dailysitestockusage'),

    path('payment-methods/', views.get_payment_methods, name='get_payment_methods'),
    path('employees/', views.get_employees, name='get_employees'),


    path('logos/', views.logo_list_create, name='logo-list-create'),
    path('logos/<int:pk>/', views.logo_detail, name='logo-detail'),





#   path('project-schedulehistory/<int:pk>/', views.project_schedulehistory, name='project_schedulehistory'),
#   path('add-project-schedulehistory/<int:pk>/', views.add_project_schedulehistory, name='add_project_schedulehistory'),
# urls.py









]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header = "CONSTRUCTION"
admin.site.site_title = "Construction"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)







