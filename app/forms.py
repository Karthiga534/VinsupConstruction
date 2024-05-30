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

