from .models import *
from django import forms
from .serializer import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from .models import ProjectCategory,Uom,EmpRoles,Employee,VendorRegistration

#-------------------------------------------------------------------- Dharshini ----------------------------------------------------------------

#------------------------------------------------------------- Custom User -------------------------------------------------------------

# class LoginForm(forms.Form):
#     email = forms.CharField(widget=forms.EmailInput)
#     password = forms.CharField(widget=forms.PasswordInput)

# class LoginForm(forms.Form):
#     email = forms.CharField(widget=forms.EmailInput, required=False)
#     phone_number = forms.CharField(required=False)
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get("email")
#         phone_number = cleaned_data.get("phone_number")
        
#         if not email and not phone_number:
#             raise forms.ValidationError("Please enter either an email or a phone number.")
        
#         return cleaned_data

# class LoginForm(forms.Form):
#     identifier = forms.CharField(label='Email or Phone Number')
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):
#         cleaned_data = super().clean()
#         identifier = cleaned_data.get("identifier")
        
#         if not identifier:
#             raise forms.ValidationError("Please enter either an email or a phone number.")
        
#         return cleaned_data

class LoginForm(forms.Form):
    identifier = forms.CharField(label='Email or Phone Number')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_identifier(self):
        identifier = self.cleaned_data.get("identifier")

        if not identifier:
            raise forms.ValidationError("Please enter either an email or a phone number.")
        
        try:
            validate_email(identifier)
            is_email = True
        except ValidationError:
            is_email = False

        if not is_email:
            if not identifier.isdigit() or len(identifier) != 10:  # Assuming phone numbers are 10 digits
                raise forms.ValidationError("Please enter a valid phone number or email address.")

        return identifier



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
