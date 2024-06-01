

from app.auth_api import *
from django.urls import path

from app import html
from .auth_ser import EmpCRUD


# employees

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'employees', EmpCRUD)



urlpatterns = [
# mobile api authentications
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='mobile-login'),
    path('login-employee/', login_employee, name='login-employee'), 
    path('generate_otp/', generate_otp, name='generate_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('reset_confirm/', reset_confirm, name='reset_confirm'),
    path('logintoken/',login_with_token_and_pin, name='login_with_token_and_pin'),
]





# superuser 
urlpatterns += [
    path('login-admin',html.login_admin,name="login-admin"),
    path('logout-admin',html.logout_admin,name="logout-admin"),
    path('v-dashboard',html.Index, name="admin-dashboard"),
    
    path('user-registration',html.register_user, name="user-registration"),

    path('remove-user/<int:pk>/',html.remove_user,name="remove-user"),
    path('edit-user/<int:pk>/',html.edit_user,name="edit-user"),  
    # admin page
    # path('',html.Index, name="admin-dashboard"),

    # superadmin page
    path('super-users',html.super_users, name="super-users"),


    path('test',html.test,name='test'),



    path('update-user/<int:pk>/',html.update_user,name="update-user"),

    
    path('create-user/',html.register_customuser,name="create-user"),
    # make superuser
    path('admin-users-upgrade/<int:pk>/',html.upgrade_admin_user, name="admin-users-upgrade"),

    # add branch
    path('add_branch/<int:pk>/' ,html.add_branch,name="add-branch")


]



urlpatterns+=router.urls