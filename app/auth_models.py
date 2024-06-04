
from .utils import *
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin, User 
today_date = timezone.now().date()




# date_format =settings.DATE_FORMAT
date_format = "%Y-%m-%d"


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

today_date = timezone.now().date()


def validate_unique_email(email):
    if email:
        try:
            existing_user = CustomUser.objects.get(email=email)
            if existing_user :
                raise ValidationError(_('This email address is already in use.'))
            else:
                pass
        except CustomUser.DoesNotExist:
            pass

        
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, pin=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        
        # Normalize the phone number
        phone_number = self.normalize_phone_number(phone_number)
        
        # Create the user object with extra fields
        user = self.model(phone_number=phone_number, **extra_fields)
        
        # Set the user's password
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        # Set the user's pin if provided
        user.pin = pin
        
        # Save the user object to the database
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, pin=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # Create the user object and set the password
        user = self.create_user(phone_number, password, pin, **extra_fields)
        return user

    def normalize_phone_number(self, phone_number):
        normalized_phone_number = phone_number.replace(" ", "").replace("-", "")
        return normalized_phone_number

class CustomUser(AbstractBaseUser, PermissionsMixin):    
    email=models.EmailField(null=True, blank=True,unique=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    # company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    pin = models.CharField(max_length=6, null=True, blank=True) 
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_owner=models.BooleanField(default=False)
    created_at =models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at =models.DateField(auto_now_add=True)
    proof=models.FileField(upload_to="proof/", null=True, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']
    disable = models.BooleanField(default=False)
    
    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        # self.pin= 1111
        super().save(*args, **kwargs)

    
    def clean(self):
        super().clean()
        if self.email is None and self.phone_number is None:
            raise ValidationError(_('Either Email or Phone Number must be set'))

    def __str__(self):
        return f"{self.name} - {self.phone_number}"
    
    # @property
    # def employee(self):
    #     if self.employee_set.all().last():
    #         return self.employee_set.all().last()
    #     return


    # @property
    # def company(self):
    #     if self.admin:
    #         if self.company_set.all().last():
    #             return self.company_set.all().last()
    #     if self.employee:
    #         return self.employee.company
    #     return
    
    @property
    def getcompanies(self):
        if self.owner:
            if self.owner_company.all().last():
                return self.owner_company.all()
        return
    

    @property
    def owner(self):
        if self.is_owner:
            if self.ownerinfo_set.all().last():
                return self.ownerinfo_set.all().last()
        return 


    
    @property
    def company(self):
        print(self.is_employee)
        if self.admin:
            return self.company_set.all().last()
        if self.is_employee:
            if self.employee_set.all():
                return self.employee_set.all().last().company
        return None  

    @property
    def employee(self):
        if self.employee_set.all():
            return self.employee_set.all().last()
        return None
    
    @property
    def get_companies(self):
        if self.admin:
            return self.company_set.all()
        return [] 



class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otp_user_details')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.otp



# ------------------------ System ------------------------

class CompanyPlan(models.Model):
    name =models.CharField(max_length=256)
    code =models.IntegerField(null=True,blank=True)

    def __str__(self) :
        if self.name:
            return self.name 
        return f'{self.__class__.__name__} Object ({self.pk})'
    
    @property
    def display(self):
        if self.name:
            return self.name
        return  
       
    @property
    def get_limits(self):
        if self.companyplanlimits_set.all():
            return self.companyplanlimits_set.all().last()
        return


class AssetType(models.Model):
    name=models.CharField(max_length=256)
    code =models.IntegerField(null=True,blank=True)
    limit= models.IntegerField(null=True,blank=True,default=1)

    def __str__(self):
        return self.name
    

class CompanyPlanLimits(models.Model):
    plan = models.ForeignKey(CompanyPlan,null=True,blank=True,on_delete=models.CASCADE)
    logo = models.IntegerField(null=True,blank=True)
    banner  = models.IntegerField(null=True,blank=True)
    active_banner =models.IntegerField(null=True,blank=True)
    employee = models.IntegerField(null=True,blank=True)
    customer = models.IntegerField(null=True,blank=True)
    documents = models.IntegerField(null=True,blank=True)


    def __str__(self) :
        if self.plan:
            return self.plan.display
        return f'{self.__class__.__name__} Object ({self.pk})'
    

    @classmethod
    def is_valid_asset(cls, limits_instance, asset_type_code):
        asset_type_fields = {
            0: 'logo',
            1: 'banner',
            2: 'active_banner',
          
        }
        if asset_type_code not in asset_type_fields:
            raise ValueError(f"Invalid asset type code: {asset_type_code}")

        field_name = asset_type_fields[asset_type_code]
        asset_count = getattr(limits_instance, field_name)

        # print(field_name,asset_count)
        return asset_count 




# --------------- directories ---------------------------

def user_directory_path(instance,filename):
   print(instance.type)
   path='company/{0}/{1}_{2}'.format(instance.company.name,instance.type.name,filename)
   return path


#------------------------------------------------------------------------- Company ---------------------------------------------------------------
# class Company(models.Model):
#     owner = models.ForeignKey(CustomUser,related_name="owner_company",null=True,blank=True,on_delete=models.CASCADE)
#     admin = models.ForeignKey(CustomUser,null=True,blank=True,on_delete=models.CASCADE)
#     name = models.CharField(max_length=500,null=True,blank=True)
#     email=models.CharField(max_length=500,null=True,blank=True)
#     phone=models.CharField(max_length=10, unique=True,null=True,blank=True)
#     address=models.TextField(null=True,blank=True)
#     gst = models.CharField(max_length=500,null=True,blank=True)
#     created_at = models.DateField(auto_now_add=True)
#     plan =models.ForeignKey(CompanyPlan,null=True,blank=True,on_delete=models.CASCADE)
#     monthly_working_days =models.IntegerField(null=True, blank=True)
#     monthly_paid_leaves =models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return self.name
    

#     @property
#     def stock(self):
#         if self.inventorystock_set.all():
#             return self.inventorystock_set.all()
#         return None 


#     def save(self, *args, **kwargs):
#         if not self.plan:
#             self.plan,_ =CompanyPlan.objects.get_or_create(code=0)
        
#         return  super().save(*args, **kwargs)

       
#     def __str__(self):
#         return str(self.name)
    

#     @property
#     def get_limits(self):
#         if self.plan:
#             return self.plan.get_limits
#         return 
    

#     @property
#     def assetlist(self):
#         if self.companyasset_set.all():
#                 return self.companyasset_set.all()
#         return None
    

#     @property
#     def assetlimit(self):
#         if self.companyassetlimit_set.all():
#                 return self.companyassetlimit_set.all()
#         return None
    

#     @property
#     def get_employees(self):
#         if self.employee_set.all():
#             return self.employee_set.all()
#         return None
    

#     # @property
#     # def get_units(self):
#     #     if self.unit_set.all():
#     #         return self.unit_set.all()
#     #     return None
    

#     # @property
#     # def get_active_unit(self):
#     #     if self.unit_set.all():
#     #         return self.unit_set.all().filter(active_sale=True).last()
#     #     return None

class Company(models.Model):
    owner = models.ForeignKey(CustomUser,related_name="owner_company",null=True,blank=True,on_delete=models.CASCADE)
    admin = models.ForeignKey(CustomUser,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=500,null=True,blank=True)
    email=models.CharField(max_length=500,null=True,blank=True)
    phone=models.CharField(max_length=10, unique=True,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    gst = models.CharField(max_length=500,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    plan =models.ForeignKey(CompanyPlan,null=True,blank=True,on_delete=models.CASCADE)
    monthly_working_days =models.IntegerField(default=26,null=True, blank=True)
    monthly_paid_leaves =models.IntegerField(default=1,null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.plan:
            self.plan,_ =CompanyPlan.objects.get_or_create(code=0)
        
        return  super().save(*args, **kwargs)

       
    def __str__(self):
        return str(self.name)
    

    @property
    def get_limits(self):
        if self.plan:
            return self.plan.get_limits
        return 
    

    @property
    def assetlist(self):
        if self.companyasset_set.all():
                return self.companyasset_set.all()
        return None
    

    @property
    def assetlimit(self):
        if self.companyassetlimit_set.all():
                return self.companyassetlimit_set.all()
        return None
    

    @property
    def get_employees(self):
        if self.employee_set.all():
            return self.employee_set.all()
        return None
    

    @property
    def get_units(self):
        if self.unit_set.all():
            return self.unit_set.all()
        return None
    

    @property
    def get_active_unit(self):
        if self.unit_set.all():
            return self.unit_set.all().filter(active_sale=True).last()
        return None




class OwnerInfo(models.Model):
    owner=models.ForeignKey(CustomUser,null=True,blank=True,on_delete=models.CASCADE)
    proof=models.FileField(upload_to="proof/", null=True, blank=True)
    address =models.TextField(null=True,blank=True)


    def set_owner(self, owner):
        # Your logic to set the owner info owner
        self.owner = owner
        self.save()




class CompanyAssetLimit(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE, null=True,blank=True)
    type=models.ForeignKey(AssetType,on_delete=models.CASCADE, null=True,blank=True)
    limit= models.IntegerField(default=5)
    
class CompanyAsset(models.Model):
    type=models.ForeignKey(AssetType,on_delete=models.CASCADE, null=True,blank=True)
    file=models.FileField(upload_to=user_directory_path, null=True, blank=True)
    company=models.ForeignKey(Company,on_delete=models.CASCADE, null=True,blank=True)
    active =models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        if self.active and self.type:
            if self.type.code == 0:
                CompanyAsset.objects.filter(company=self.company,type__code = 0, active=True).exclude(pk=self.pk).update(active=False)
            if self.type.code == 1:
                obj =  CompanyAsset.objects.filter(
                    company=self.company,
                    type__code=1,
                    active=True
                )
                active_count = obj.count()
                try :
                    active_limit = self.company.get_limits.active_banner
                except :
                    active_limit = 0
                if active_count >= active_limit:
                    oldest_asset = obj.order_by('id').first()
                    oldest_asset.active = False
                    oldest_asset.save(update_fields=['active'])
        super().save(*args, **kwargs)


    @property
    def gettype(self):
        if self.type:
                return self.type
        return
    
    @property
    def asset_limit(self):
        if self.company:
                if self.company.assetlimit :
                    return self.company.assetlimit.filter(type=type).last().limit
        return None
    
class City(models.Model):
    name = models.CharField(max_length=30)
    company=models.ForeignKey(Company,on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.name
    






class Employees(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=50,null=True,blank=True)   
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    bankname=models.CharField(max_length=50,null=True,blank=True)
    branch=models.CharField(max_length=50,null=True,blank=True)
    bankaccount=models.CharField(max_length=50,null=True,blank=True)
    ifsccode=models.CharField(max_length=50,null=True,blank=True)
    start_date=models.DateField(auto_now_add=True, null=True, blank=True)
    wage=models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)


