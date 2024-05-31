from .models import *
from django import forms
from .serializer import *
from django.core.validators import MaxLengthValidator
from .models import ProjectCategory,Uom,EmpRoles,Employee,VendorRegistration
#-------------------------------------------------------------------- Dharshini ----------------------------------------------------------------

#------------------------------------------------------------- Custom User -------------------------------------------------------------

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

#------------------------------------------------------------- Company Staff -------------------------------------------------------------

class EmpRolesForm(forms.ModelForm):
    class Meta:
        model = EmpRoles
        fields = ['name','description']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name','role','address','bankname','branch','bankaccount','ifsccode']



#-------------------------------------------------------------------- End Dharshini ----------------------------------------------------------------

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=255 ,required=True)
    phone_number = forms.CharField(max_length=10 ,required=True)
    address = forms.CharField(max_length=255,required=True)
    proof = forms.FileField(required=True)  # Add the file field for proof document upload

    company_email = forms.EmailField(required=True)
    company_name = forms.CharField(max_length=255 ,required=True)
    company_phone_number = forms.CharField(max_length=10 ,required=True)
    company_address = forms.CharField(max_length=255,required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone_number', 'address', 'proof' , "company_email","company_name","company_phone_number","company_address"]
