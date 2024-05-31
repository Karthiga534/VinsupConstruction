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

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)


class SetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data