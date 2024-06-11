import uuid
from .utils import *
from decimal import Decimal
from django.db import models
from app.auth_models import *
from django.db.models import Q
from django.db.models import Sum
from django.utils import timezone
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError


today_date = timezone.now().date()

DUTY_HOURS = 8

# date_format =settings.DATE_FORMAT
date_format = "%Y-%m-%d"


# ------------------------------------------------------------ system  library ------------------------------------------------------------

class WorkStatus(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class ProcessStatus(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    classname = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

class PaymentStatus(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
   

    def __str__(self):
        return self.name

class ContractType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Duration(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=256, null=True, blank=True)


    def __str__(self):
        return self.name

class Priority(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    


    def __str__(self):
        return self.name
    
class PaymentSchedule(models.Model):
    days = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.days if self.days else 0)


# --------------------------------------------------------------------------------------


#------------------------------------------------------------------- CustomUser ----------------------------------------------------------------
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# today_date = timezone.now().date()


# def validate_unique_email(email):
#     if email:
#         try:
#             existing_user = CustomUser.objects.get(email=email)
#             if existing_user :
#                 raise ValidationError(_('This email address is already in use.'))
#             else:
#                 pass
#         except CustomUser.DoesNotExist:
#             pass


# class CustomUserManager(BaseUserManager):
#     def create_user(self, phone_number, password=None, pin=None, **extra_fields):
#         if not phone_number:
#             raise ValueError('The phone number must be set')
#         user = self.model(phone_number=self.normalize_phone_number(phone_number), **extra_fields)
       
#         user.pin = pin
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, phone_number, password=None, pin=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(phone_number, password, pin, **extra_fields)

#     def normalize_phone_number(self, phone_number):
#         normalized_phone_number = phone_number.replace(" ", "").replace("-", "")
#         return normalized_phone_number
 
# class CustomUser(AbstractBaseUser, PermissionsMixin):    
#     email=models.EmailField(null=True, blank=True)
#     image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
#     name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=10, unique=True)
#     # company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
#     pin = models.CharField(max_length=6, null=True, blank=True) 
#     is_active = models.BooleanField(default=True)
#     admin = models.BooleanField(default=False)
#     is_employee = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     otp = models.CharField(max_length=6, null=True, blank=True)
#     created_at =models.DateField(auto_now_add=True)
#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = ['name']
#     disable = models.BooleanField(default=False)
    
#     objects = CustomUserManager()


#     def save(self, *args, **kwargs):
#         if self.email:
#             self.email = self.email.lower()
#         # self.pin= 1111
#         super().save(*args, **kwargs)

    
#     def clean(self):
#         super().clean()
#         if self.email is None and self.phone_number is None:
#             raise ValidationError(_('Either Email or Phone Number must be set'))

#     def __str__(self):
#         return f"{self.name} - {self.phone_number}"
    
#     # @property
#     # def employee(self):
#     #     if self.employee_set.all().last():
#     #         return self.employee_set.all().last()
#     #     return


#     # @property
#     # def company(self):
#     #     if self.admin:
#     #         if self.company_set.all().last():
#     #             return self.company_set.all().last()
#     #     if self.employee:
#     #         return self.employee.company
#     #     return
    
#     @property
#     def getcompanies(self):
#         if self.owner:
#             if self.owner_company.all().last():
#                 return self.owner_company.all()
#         return
    

#     @property
#     def owner(self):
#         if self.is_owner:
#             if self.ownerinfo_set.all().last():
#                 return self.ownerinfo_set.all().last()
#         return 


    
#     @property
#     def company(self):
#         print(self.is_employee)
#         if self.admin:
#             return self.company_set.all().last()
#         if self.is_employee:
#             if self.employee_set.all():
#                 return self.employee_set.all().last().company
#         return None  

#     @property
#     def employee(self):
#         if self.employee_set.all():
#             return self.employee_set.all().last()
#         return None
    
#     @property
#     def get_companies(self):
#         if self.admin:
#             return self.company_set.all()
#         return [] 
    
    
# #------------------------------------------------------------------------- Company ---------------------------------------------------------------
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





# class Company(models.Model):
#     name = models.CharField(max_length=50)
#     admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
#     monthly_working_days =models.IntegerField(null=True, blank=True)
#     monthly_paid_leaves =models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return self.name
    

#     @property
#     def stock(self):
#         if self.inventorystock_set.all():
#             return self.inventorystock_set.all()
#         return None   
    

    

# ------------------------------------------------------------ COMPANY MASTERS ------------------------------------------------------

# -- UOM ---------

class Uom(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=50)
    #date= models.DateField(auto_now_add=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# MATERIAL LIBRARIES

class MaterialLibrary(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    item=models.CharField(max_length=100,null=True,blank=True)
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE,null=True,blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.item
    
    @property
    def display(self):
        return self.item


    # def __str__(self):
    #     if self.item:
    #         return self.item
    #     return None

    class Meta:
        #    unique_together to enforce uniqueness across multiple fields
        unique_together = ('item', 'company', 'unit')


    @property
    def purchase_history(self):
        if self.purchaseitems_set.all():
                return self.purchaseitems_set.all()
        return None
        
class OthersLibrary(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    item=models.CharField(max_length=100,null=True,blank=True)
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE,null=True,blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    def __str__(self):
        return self.item
        

# COMPANY MACHINARY CHARGES
    
class CompanyMachinaryCharges(models.Model) :
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    payment_schedule =  models.ForeignKey(PaymentSchedule, on_delete=models.CASCADE, null=True, blank=True)
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.name


# LABOUR ROLES AND SALARY

class LabourRolesAndSalary(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    payment_schedule =  models.ForeignKey(PaymentSchedule, on_delete=models.CASCADE, null=True, blank=True)
    ot_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    date = models.DateField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return self.name

    
#------>project category 
class ProjectCategory(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

#------------- Contract category ---------

class Contractcategory(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# EMP ROLES -----

class EmpRoles(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
#----------------------------------------------------------------------- COMPANY STAFFS-----------------------------------------------------
    
# EMPLOYEE 
class Employee(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    img =models.FileField(upload_to="doc",null=True,blank=True)
    name=models.CharField(max_length=50,null=True,blank=True)
    role=models.ForeignKey(EmpRoles, on_delete=models.CASCADE,null=True,blank=True) 
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    bankname=models.CharField(max_length=50,null=True,blank=True)
    branch=models.CharField(max_length=50,null=True,blank=True)
    bankaccount=models.CharField(max_length=50,null=True,blank=True)
    ifsccode=models.CharField(max_length=50,null=True,blank=True)
    start_date=models.DateField(auto_now_add=True, null=True, blank=True)
    wage=models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    payment_schedule = models.ForeignKey(PaymentSchedule, on_delete=models.CASCADE, null=True, blank=True) 
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #     if self.user:
    #         user =self.user
    #         user.is_employee =True
           
    #     super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Perform validation before saving
        if self.user:
            user =self.user
            user.is_employee =True
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils.translation import gettext_lazy as _

        try:
             queryset = Employee.objects.exclude(pk=self.pk) if self else Employee.objects.all()
             if queryset.filter(mobile=self.mobile).exists():
                raise ValidationError('Mobile number already exists.')
             
            #  if CustomUser.objects.filter(phone_number=self.mobile).exists():
            #     raise ValidationError ('Already exists')
                # raise ValidationError('Mobile number already exists.')
                    # validate_mobile(self.mobile, instance=self)
        except ValidationError as e:
            raise ValidationError({'mobile': ["Already exists"]})

    @property
    def disable(self):
        if self.user:
            return self.user.disable
        return False

    @property
    def get_attendence(self):
        if self.attendance_set.all():
            return self.attendance_set.all()
        return None
    

    @property
    def get_salary_details(self):
        if self.salary_set.all():
            return self.salary_set.all()
        return None
    

    @property
    def get_payment_receipt(self):
        if self.salaryreceipt_set.all():
            return self.salaryreceipt_set.all()
        return None
    

    @property
    def this_month_paid(self, month):
        if self.get_payment_receipt:
            payments_this_month = self.get_payment_receipt.filter(payment_date__month=month)
            if payments_this_month:
                return payments_this_month
        return None

    @property
    def calculate_day_wage(self):
        return 1000  
    

    @property
    def get_allowed_leaves(self):
        return 1 
    
    @property
    def get_daily_wage(self):
        if self.get_working_days:
            return self.get_current_salary / get_int_or_zero(self.get_working_days)
        return self.get_current_salary / 26

    @property
    def get_current_salary(self):
        return get_amount_or_zero(self.monthly_salary)
        return self.salary_set.last()  # Get the latest salary
    
    def was_present_on_date(self, date_to_check):
        return True  # Assuming the employee is present for all dates for now

    # def list_unpaid_employees(self, start_date, end_date):
    #     # List employees who haven't been paid for the specified period
    #     unpaid_employees = Employee.objects.exclude(
    #         id__in=SalaryReceipt.objects.filter(
    #             payment_period_start=start_date,
    #             payment_period_end=end_date
    #         ).values_list('created_by__id', flat=True)
    #     )

    #     return unpaid_employees
    

    # def calculate_payment_for_period(self, days_to_include=None, day_wage=None):
    #     # Calculate the end date (today's date)
    #     end_date = datetime.now().date()
    #     days = days_to_include  if days_to_include else self.payment_schedule.days
    #     wage = day_wage if day_wage else self.wage


    #     # Calculate the start date based on the days_to_include
    #     start_date = end_date - timedelta(days=days)

    #     # Calculate total payment based on day wage and attendance
    #     total_payment = self.calculate_total_payment(start_date, end_date, wage)

    #     # Check if a SalaryReceipt already exists for this period
    #     existing_receipt = self.salaryreceipt_set.filter(
    #         payment_period_start=start_date,
    #         payment_period_end=end_date
    #     ).first()

    #     if existing_receipt:
    #         # A receipt already exists for this period, update it
    #         existing_receipt.amount_paid += total_payment
    #         existing_receipt.payment_period_end = end_date
    #         existing_receipt.save()
    #     else:
    #         # Create a new receipt for this period
    #         receipt = SalaryReceipt.objects.create(
    #             salary=self.get_current_salary(),
    #             created_by=self,
    #             amount_paid=total_payment,
    #             payment_period_start=start_date,
    #             payment_period_end=end_date
    #             # Other fields as needed
    #         )

    # def calculate_total_payment(self, start_date, end_date, wage):
    #     # Placeholder method to calculate total payment based on attendance
    #     total_payment = 0
    #     current_date = start_date

    #     while current_date <= end_date:
    #         # Check if the employee was present on the current date (you need to implement this logic)
    #         if self.was_present_on_date(current_date):
    #             total_payment += wage

    #         current_date += timedelta(days=1)

    #     return total_payment



    @property
    def get_today_attendence(self):
        project = None
        clock_in = None
        clock_out = None
        overtime = None
        project_name = None
        fdate =None
        present =False
        atten_id =  0
        today =get_today()
     
        if self.get_attendence and self.get_attendence.exists():
            today =self.get_attendence.filter(date=today).last()
            print(today,"today")
            if today:
                clock_in =today.clock_in
                clock_out =today.clock_out
                overtime =today.over_time
                present = True if today.clock_in else False
                project = today.project.id if today.project else None
                project_name=today.project.display if today.project else None
                fdate =today
                atten_id=today.id
                
        return project,project_name,clock_in,clock_out,overtime,present,atten_id


    @property
    def get_working_days(self,month=None):

        try:
            if self.company.monthly_working_days:
                return int(self.company.monthly_working_days)
            else:return 26
    
        except:
            return 26
    
    @property
    def monthly_working_days(self,month=None):
        try:
            if self.company.monthly_working_days :
                return int(self.company.monthly_working_days )
            else:return 26
        except:
            return 26

    # @property
    def this_month_salary(self,date=None):
        # current_month = timezone.now().date().replace(day=1)
        # next_month = (current_month + timedelta(days=32)).replace(day=1)
        date = date if date else get_today()
        base_salary = get_amount_or_zero(self.get_current_salary)
        net_salary = base_salary

        start_date,end_date=get_month_start_and_end(date)

        working_days = self.get_working_days

        active_working_days =  self.monthly_working_days 
        

        # paid_working_days = self.get_working_days - self.monthly_working_days 
        paid_working_days = get_int_or_zero(self.company.monthly_paid_leaves)
 
        present_days = Attendance.objects.filter(
            employee=self, 
            date__range=(start_date, end_date), 
            present=True
        ).count()

        leaves_taken = active_working_days - present_days 
       
        leave_allowed = 0 if active_working_days - leaves_taken <=0 else self.get_allowed_leaves

        # print(leave_allowed,self)
    
        day_wage = get_amount_or_zero(base_salary) / get_amount_or_zero(working_days)

      
        loss_of_pay =(((leaves_taken - leave_allowed)+ paid_working_days) * day_wage )  
        # print(loss_of_pay,"lodss")
        net_salary =net_salary - get_amount_or_zero(loss_of_pay)
        
        # SalaryReceipt.objects.get_or_create(payment_period_start =start_date,payment_period_end=end_date)
        salary_receipts = SalaryReceipt.objects.filter(employee=self)
        is_paid = salary_receipts.filter(
            Q(payment_period_start__gte=start_date) & Q(payment_period_end__lte=end_date)
        )
       
        paid=0
        pending= net_salary
        if is_paid:
            for i in is_paid:
                paid +=i.amount_paid
                pending -=i.amount_paid

        start_date=get_date(start_date)
        end_date =get_date(end_date)
        ispaid =False if paid < net_salary  else True
        net_salary = "{:.2f}".format(net_salary)
        pending = "{:.2f}".format(pending)
        return net_salary ,paid,pending ,start_date , end_date,ispaid
    


    def get_paid_and_pending(self,date=None):
        date = date if date else timezone.now().date()
        # start_date,end_date=get_month_start_and_end(date)
        salary,start_date,end_date=self.this_month_salary(date)

        salary_receipts = SalaryReceipt.objects.filter(employee=self)

      
        is_paid = salary_receipts.filter(
            Q(payment_period_start__lte=start_date) & Q(payment_period_end__gte=end_date)
        )

        if is_paid:
            return  is_paid.get_paid_amount,is_paid.get_pending_amount
        
        return 0,salary

# COMPANY LABOUR MODEL
class CompanyLabours(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    image = models.FileField(upload_to='company-labour/', null=True, blank=True)
    role = models.ForeignKey(LabourRolesAndSalary, on_delete=models.CASCADE, null=True, blank=True)
    company_rate = models.BooleanField(default=False)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    payment_schedule =  models.ForeignKey(PaymentSchedule, on_delete=models.CASCADE, null=True, blank=True)
    ot_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    disable = models.BooleanField(default=False)
    
    # @property
    def __str__(self):
        return str(f"{self.name}" if self.name else "unnamed")
    
    @property
    def display(self):
        return f'{self.name}'
    

    @property
    def is_company_rate(self):
        if self.company_rate:
            return True
        return False

    def get_wage(self):
        if self.rate and self.payment_schedule:
            return get_amount_or_zero( self.rate) *   get_amount_or_zero(self.payment_schedule.days)
        return 0
    
    @property
    def get_rate(self):
        if self.company_rate:
            print(self.role.name)
            return get_amount_or_zero(self.role.rate)
        return get_amount_or_zero(self.rate)
    

    @property
    def get_payment_schedule(self):
        if self.company_rate:
            return self.role.payment_schedule
        return self.payment_schedule
    
    @property
    def get_ot_rate(self):
        return get_amount_or_zero(self.get_rate) / DUTY_HOURS
    


    @property
    def get_attendence(self):
        if self.projectlabourattendence_set.all():
            return self.self.projectlabourattendence_set.all()
        return None
    

    # class ProjectLabourAttendence(models.Model):
    # company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    # labour = models.ForeignKey(CompanyLabours, on_delete=models.CASCADE, null=True, blank=True)
    # over_time = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)
    # clock_in=models.TimeField(null=True, blank=True)
    # clock_out=models.TimeField(null=True, blank=True)
    # date=models.DateField(null=True,blank=True)
    # present=models.BooleanField(default=False)
    
    @property
    def get_today_attendence(self):
        project = None
        clock_in = None
        clock_out = None
        overtime = None
        project_name = None
        fdate =None
        present =False
        atten_id =  0
        today =get_today()
     
        if self.projectlabourattendence_set.exists():
            today =self.projectlabourattendence_set.filter(date=today).last()
            print(today,"today")
            if today:
                clock_in =today.clock_in
                clock_out =today.clock_out
                overtime =today.over_time
                present = True if today.clock_in else False
                project = today.project.id if today.project else None
                project_name=today.project.display if today.project else None
                fdate =today
                atten_id=today.id
                
        return project,project_name,clock_in,clock_out,overtime,present,atten_id


    @property
    def salary_for_presented_days(self):

        attendance_records = ProjectLabourAttendence.objects.filter(labour=self, present=True)

        salary_receipts = SalaryReceipt.objects.filter(labour=self)

        total_salary = 0
        for record in attendance_records:
            is_paid = salary_receipts.filter(
                Q(payment_period_start__gte=record.date) & Q(payment_period_end__lte=record.date)
            ).exists()
            if not is_paid:
                total_salary += self.get_rate
        
        return total_salary


    @property
    def total_salary_for_presented_days(self):
   
        attendance_records = ProjectLabourAttendence.objects.filter(labour=self, present=True)

        salary_receipts = SalaryReceipt.objects.filter(labour=self)

        start=False
        start_date =get_today()
        end_date =get_today()
      
        total_salary = 0
        days=0

        present_days = [i.date for i in attendance_records]

        payement_dates = []

        
        for record in attendance_records:
            print(record.date,"pppppppppppppp")
            for i in salary_receipts:
                print(i.payment_period_start ,i.payment_period_end ,"lllllllllllllllllllllllllllllll")

            is_paid = salary_receipts.filter(
            Q(payment_period_start__lte=record.date) & 
            Q(payment_period_end__gte=record.date)
        ).exists()
            print()

            print(is_paid,"is_paid")
    
            if not is_paid:
                daily_salary = self.get_rate
                if record.over_time:
                    daily_salary += record.over_time * self.get_ot_rate
                total_salary += daily_salary
              
                payement_dates.append(record.date)

                days +=1
        is_pending = True  if  self.get_salary_receipts and total_salary >=0 else False
        if payement_dates:
            payement_dates.sort()
            start_date =payement_dates[0]
            end_date=payement_dates[-1]
        
        return total_salary ,start_date,end_date,days,is_pending
    

    @property
    def get_salary_receipts(self):
        if self.salaryreceipt_set.all():
            return self.salaryreceipt_set.all()
        return None

    @property
    def get_paid_amount(self):
        amount=0
        if self.get_salary_receipts:
            amount = sum(i.get_paid_amount for i in self.get_salary_receipts )
            
        return amount
        

    @property
    def get_pending_amount(self):
        amount=0
        if self.get_salary_receipts:
            # return self.get_salary_receipts.get_pending_amount
            amount = sum(i.get_pending_amount for i in self.get_salary_receipts )
            return amount   
        
        return self.total_salary_for_presented_days[0]
    


#----------------------------------------------------------------------- VENDOR MANAGEMENT -------------------------------------------------------

#---------------> Vendor Registration 

class VendorRegistration(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    vendorname = models.CharField(max_length=25,null=True, blank=True)
    companyname = models.CharField(max_length=100,null=True, blank=True)
    gstno = models.CharField(max_length=25,null=True, blank=True)
    mobile = models.CharField(max_length=13,null=True, blank=True)
    email = models.EmailField(max_length=150,null=True, blank=True)
    faxno = models.CharField(max_length=25,null=True, blank=True)
    address = models.CharField(max_length=250,null=True, blank=True)

    def __str__(self):
        return self.vendorname  
    
    @property
    def display(self):
        if self.vendorname:
            return self.vendorname
        if self.companyname:
            return self.companyname
        return self.email or "unnamed"
    
#---------------> Vendor Quatation

class VendorQuatation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    vendorname = models.ForeignKey(VendorRegistration, on_delete=models.CASCADE, null=True, blank=True)
    quatationno = models.CharField(max_length=100)
    quatationamount = models.CharField(max_length=50)
    img = models.FileField(upload_to="doc")
    # mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.quatationno 
    

# ------------------------------------------------------------Contractor------------------------------------------------------------

class Contractor(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    contact_no = models.CharField(max_length=15,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    area = models.CharField(max_length=100,null=True,blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE,null=True,blank=True)
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    maistry = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    maison_cooli = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    male_skilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    male_unskilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    female_skilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    female_unskilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Contractcategory, on_delete=models.CASCADE,null=True,blank=True)
    start_date=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    @property
    def display(self):
        if self.name :
            return self.name
        return "unnamed"    
    

# -------------------------------------------- project ------------------------------------------------------------------------

class Project(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    proj_id=models.CharField(max_length=100,null=True,blank=True)
    client = models.CharField(max_length=100,null=True,blank=True)
    contact_no = models.CharField(max_length=15,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    proj_name=models.CharField(max_length=100,null=True,blank=True)
    site_location=models.CharField(max_length=100,null=True,blank=True)
    incharge=models.ForeignKey(Employee, on_delete=models.CASCADE,null=True,blank=True)  #dropdown
    start_date=models.DateField(null=True,blank=True)
    end_date =models.DateField(null=True,blank=True)
    duration =models.ForeignKey(Duration, on_delete=models.CASCADE,null=True,blank=True)
    priority =models.ForeignKey(Priority, on_delete=models.CASCADE,null=True,blank=True)
    estimation=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    modeldesign =models.FileField(upload_to="doc")
    aggeaments =models.FileField(upload_to="doc")
    proj_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE,null=True,blank=True)
    status = models.ForeignKey(WorkStatus, on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(null=True,blank=True) 
    terms_conditions = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.proj_name} - {self.site_location}"
    
    @property
    def display(self):
        if self.proj_name and self.site_location:
            return self.proj_name + "--" +self.site_location
        if self.proj_name:
            return self.proj_name
        if self.client:
            return self.client
        return self.proj_id 

    @property
    def stock(self):
        if self.sitestock_set.all():
            return self.sitestock_set.all()
        return None
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only set the default status for new projects
            default_status = WorkStatus.objects.filter(code="-2").last()
            if default_status:
                self.status = default_status
        super().save(*args, **kwargs)
        

    @property
    def expenses(self):
        amount =0 

        amount =self.purchace_expense + self.site_expense +self.subcontract_expense+self.employee_salary+self.labour_salary
        # # expense
        # if self.expense_set.all():
        #     amount += sum(get_amount_or_zero(invoice.amount) for invoice in self.expense_set.all())
        # # purchase
        # if self.purchaseinvoice_set.all():
        #     amount += sum(get_amount_or_zero(invoice.total_amount) for invoice in self.purchaseinvoice_set.all())
        # # subcontract
        # if self.projectsubcontract_set.all():
        #     amount += sum(get_amount_or_zero(invoice.get_paid_amount) for invoice in  self.projectsubcontract_set.all())
        # # employee salary
        # if self.incharge and self.incharge.get_salary_details:
        #     amount += sum(get_amount_or_zero(invoice.amount) for invoice in self.incharge.get_salary_details)
        # # labour
        # if self.incharge and self.incharge.get_salary_details:
        #     amount += sum(get_amount_or_zero(invoice.amount) for invoice in self.incharge.get_salary_details)

        return amount
    

    @property
    def purchace_expense(self):
        amount =0 
        if self.purchaseinvoice_set.all():
            amount += sum(get_amount_or_zero(invoice.total_amount) for invoice in self.purchaseinvoice_set.all())

        return amount
    

    @property
    def site_expense(self):
        amount =0 
        if self.expense_set.all():
            amount += sum(get_amount_or_zero(invoice.amount) for invoice in self.expense_set.all())

        return amount

    @property
    def subcontract_expense(self):
        amount =0 
        if self.projectsubcontract_set.all():
            amount += sum(get_amount_or_zero(invoice.get_paid_amount) for invoice in  self.projectsubcontract_set.all())

        return amount
    

    @property
    def employee_salary(self):
        # get_wage
        amount =0 
        if self.get_employee_attendence:
            amount += sum( get_amount_or_zero(i.get_wage) for i in self.get_employee_attendence )
        # if self.incharge and self.incharge.get_salary_details:
        #     amount += sum(get_amount_or_zero(invoice.amount) for invoice in self.incharge.get_salary_details)
        return amount
    

    @property
    def get_labour_attendence(self):
        if self.projectlabourattendence_set.all():
            return  self.projectlabourattendence_set.all()
        return None
    
    @property
    def get_employee_attendence(self):
        if self.attendance_set.all():
            return  self.attendance_set.all()
        return None
    

    @property
    def labour_salary(self):
        amount =0 
        if self.get_labour_attendence:
            amount += sum( get_amount_or_zero(i.get_wage) for i in self.get_labour_attendence )
        # if self.get_labour_attendence and self.incharge.get_salary_details:
        #     amount += sum(get_amount_or_zero(invoice.amount) for invoice in self.incharge.get_salary_details)

        return amount
    

    @property
    def loss_or_profit(self):
        amt =self.estimation - self.expenses
        if amt >0 :
            return amt
        return amt
    

    @property
    def total_purchase_amount(self):
        pamount=0
        purchasehistory=self.purchaseinvoice_set.all()
        print(purchasehistory)
        if purchasehistory:
            pamount =sum( get_amount_or_zero(i.total_amount) for i in purchasehistory) 
        return pamount
    


    @property
    def total_purchase_paid_amount(self):
        pamount=0
        purchasehistory=self.purchaseinvoice_set.all()
        print(purchasehistory)
        if purchasehistory:
            pamount =sum( get_amount_or_zero(i.paid) for i in purchasehistory) 
        return pamount
    

    @property
    def total_purchase_pending_amount(self):
      return self.total_purchase_amount -self.total_purchase_paid_amount



# ----------------------------- stock management ---------------------------------- ---------------------------------------------------- 


class InventoryStock(models.Model):
    company=models.ForeignKey(Company,related_name='inventory_stocks', on_delete=models.CASCADE,null=True,blank=True)
    item=models.ForeignKey(MaterialLibrary, on_delete=models.CASCADE,null=True,blank=True)
    name= models.CharField(max_length=255,null=True,blank=True)
    total_supplied_qty=models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    qty=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)    #add  with purchase qty
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE,null=True,blank=True)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    taken_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    date = models.DateField(auto_now_add=True, null=True, blank=True)
    # def __str__(self):
    #     if self.name:
    #         return self.name
    #     return None

    def save(self, *args, **kwargs):
        if not self.total_supplied_qty:
           self.total_supplied_qty =self.qty
        super().save(*args, **kwargs)

    @property
    def get_total(self):
        total = self.qty * self.price
        return  "{:.2f}".format(total)
    
    @property
    def available_qty(self):
        total = self.total_supplied_qty - self.taken_qty
        return  "{:.2f}".format(total)
    

    
    @property
    def display(self):
        if self.item:
            return self.item.item
        if self.name:
            return self.name
        return None
    
    @property
    def purchase_history(self):
        if self.item:  
            if self.item.purchase_history:
                return self.item.purchase_history
        return None

        
class DailyInventoryUsage(models.Model):
    stock=models.ForeignKey(InventoryStock, on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    material = models.ForeignKey(MaterialLibrary, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    used = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.material} - {self.date}"  


class SiteStock(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    inventory=models.ForeignKey(InventoryStock, on_delete=models.CASCADE,null=True,blank=True)
    item=models.ForeignKey(MaterialLibrary, on_delete=models.CASCADE,null=True,blank=True)
    name= models.CharField(max_length=255,null=True,blank=True)
    total_supplied_qty=models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    qty=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)    #qty
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE,null=True,blank=True)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    taken_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date = models.DateField(auto_now_add=True, null=True, blank=True)


    # def __str__(self):
    #     return self.name

    class Meta:
        # Define unique_together to enforce uniqueness across multiple fields
        unique_together = ('item', 'company', 'unit','project')

    def save(self, *args, **kwargs):
        if not self.total_supplied_qty:
           self.total_supplied_qty =self.qty
        super().save(*args, **kwargs)

    @property
    def get_total(self):
        total = self.qty * self.price
        return  "{:.2f}".format(total)
    


    
    @property
    def available_qty(self):
        total = self.total_supplied_qty - self.taken_qty
        return  "{:.2f}".format(total)
    

    @property
    def purchase_history(self):
        if self.item:  
            if self.item.purchase_history:
                return self.item.purchase_history
        return None
    

    @property
    def display(self):
        if self.item:  
       
            return self.item.item
        return None



class DailyMaterialUsage(models.Model):
    stock=models.ForeignKey(SiteStock, on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    material = models.ForeignKey(MaterialLibrary, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    used = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.material} - {self.date}"

# --------------------------------- PURCHASE ------------------------------------------------------------


class PurchaseInvoice(models.Model):
    site = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    vendor = models.ForeignKey(VendorRegistration, on_delete=models.CASCADE,null=True,blank=True)
    company= models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    vendor_company=models.CharField(max_length=255,null=True,blank=True)
    gst= models.CharField(max_length=255,null=True,blank=True)
    tax= models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    contact_no= models.CharField(max_length=255,null=True,blank=True)
    invoice_id=models.CharField(max_length=255,null=True,blank=True)
    created_at=models.DateField()
    total_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    paid=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    pending=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    status = models.ForeignKey(ProcessStatus, on_delete=models.CASCADE,null=True,blank=True)
    is_delivered = models.BooleanField(default=False)
    
    class Meta:
        # Define a unique constraint to enforce uniqueness of invoice_id per company
        unique_together = ('invoice_id', 'company')


    
    def clean(self):
        super().clean()

        if self.invoice_id and self.company_id is not None:
            existing_invoices = PurchaseInvoice.objects.filter(
                invoice_id=self.invoice_id,
                company=self.company
            ).exclude(pk=self.pk)  # Exclude the current instance if updating
            if existing_invoices.exists():
                raise ValidationError({'invoice_id': ['An invoice with this ID already exists for this company.']})


    def save(self, *args, **kwargs):
        self.full_clean()  #
        if not self.status:
            self.status,_ =ProcessStatus.objects.get_or_create(code=2)
        if not self.invoice_id:
            # Generate or set the invoice_id if not already provided
            # You can generate it based on your specific requirements
            # For example, combining company_id with a unique identifier
            self.invoice_id = f'{self.company_id}-{self.generate_unique_identifier()}'
        super().save(*args, **kwargs)


    def generate_unique_identifier(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


    # def __str__(self):
    #     return self.vendor_company
    

    @property
    def get_purchase_items(self):
        if self.purchaseitems_set.all():
            return self.purchaseitems_set.all()
        else :
            return []



class PurchaseItems(models.Model):
    invoice=models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE,null=True,blank=True)
    item=models.ForeignKey(MaterialLibrary, on_delete=models.CASCADE,null=True,blank=True)
    inventory=models.ForeignKey(InventoryStock, on_delete=models.CASCADE,null=True,blank=True)   #change
    name = models.CharField(max_length=255, null=True,blank=True)
    qty=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)   #change
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)   #change
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE,null=True,blank=True)    #change
    sub_total=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)     #change
    for_site = models.BooleanField(default=False)

    def __str__(self):
        return self.name or self.item.display
    
    @property
    def purchase_info(self):
        if self.invoice:
            return self.invoice
        return None
# ----------------------------------- QUOTATION -----------------------------------------------------------------------------        

class Quatation(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    quatation_id=models.CharField(max_length=255,null=True,blank=True)
    site=models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    start_date=models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True,blank=True)
    status = models.ForeignKey(ProcessStatus, on_delete=models.CASCADE,null=True,blank=True)
 

    #created by Employee , Status

    # def __str__(self):
    #     return self.quatation_id

    def __str__(self):
        return f"{self.quatation_id} - {self.site}"


    def save(self, *args, **kwargs):
        self.full_clean()  #
        if not self.quatation_id:
            self.quatation_id = f'{generate_unique_identifier(self.company)}{self.id}'
        super().save(*args, **kwargs)

    

    def get_quotation_items(self):
        if self.quatationitems_set.all():
            return self.quatationitems_set.all()
        else :
            return []
        
    def save(self, *args, **kwargs):
        self.full_clean()  #
        if not self.status:
            self.status,_ =ProcessStatus.objects.get_or_create(code=2)
        if not self.quatation_id:
            self.quatation_id = f'{self.company_id}-{self.generate_unique_identifier()}'
        super().save(*args, **kwargs)


    def generate_unique_identifier(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class QuatationItems(models.Model):
    invoice=models.ForeignKey(Quatation, on_delete=models.CASCADE,null=True,blank=True)
    inventory=models.ForeignKey(InventoryStock, on_delete=models.CASCADE,null=True,blank=True)   #change
    item =models.ForeignKey(MaterialLibrary,on_delete=models.CASCADE,null=True,blank=True)
    name= models.CharField(max_length=255,null=True,blank=True)
    qty=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)   #change
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE,null=True,blank=True)    #change

    def __str__(self):
         return self.name if self.name else 'Unnamed QuatationItem'
    
    @property
    def display_name(self):
        
        if self.item:
            return self.item.item
        if self.inventory:
            return self.inventory.display
        
        if self.name:
            return  self.name 
        return None


# -------------------------- TRANSFER -------------------------------------------------------------------------------------------

class TransferInvoice(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    from_site = models.ForeignKey(Project,related_name='from_project', on_delete=models.CASCADE,null=True,blank=True)
    to_site =  models.ForeignKey(Project,related_name='to_project', on_delete=models.CASCADE,null=True,blank=True)
    from_inventory =  models.ForeignKey(Company,related_name='from_company', on_delete=models.CASCADE,null=True,blank=True)
    to_inventory =  models.ForeignKey(Company,related_name='to_company', on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateField(auto_now_add=True)
    invoice_id=models.CharField(max_length=255,null=True,blank=True)
    item_delivered =models.BooleanField(default=False)
    received_by =models.ForeignKey(Employee, on_delete=models.CASCADE,null=True,blank=True)


    def save(self, *args, **kwargs):
        self.full_clean()  #
        if not self.invoice_id:
            self.invoice_id = f'{generate_unique_identifier(self.company)}{self.id}'
        super().save(*args, **kwargs)
    
    @property
    def get_transfer_items(self):
        if self.transferitems_set.all():
            return self.transferitems_set.all()
        return None

class TransferItems(models.Model):
    invoice=models.ForeignKey(TransferInvoice, on_delete=models.CASCADE,null=True,blank=True)
    item=models.ForeignKey(MaterialLibrary, on_delete=models.CASCADE,null=True,blank=True)
    inventory=models.ForeignKey(InventoryStock, on_delete=models.CASCADE,null=True,blank=True)
    name= models.CharField(max_length=255,null=True,blank=True)
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE,null=True,blank=True)
    qty=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    item_delivered =models.BooleanField(default=False)
    received_by =models.ForeignKey(Employee, on_delete=models.CASCADE,null=True,blank=True)

    @property
    def get_total(self):
        if self.qty:
            return self.qty *self.price
        return None

# --------------------------------------- salary management ----------------------------------------------------------------


# not used
class Salary(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    employee=models.ForeignKey(Employee,null=True,blank=True, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_schedule = models.ForeignKey(PaymentSchedule, on_delete=models.CASCADE, null=True, blank=True) 



# make payment receipt  for employee or user
class SalaryReceipt(models.Model):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    labour = models.ForeignKey(CompanyLabours, null=True, blank=True, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    payment_amount =  models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_period_start = models.DateField(null=True, blank=True)  # Start date of the payment period
    payment_period_end = models.DateField(null=True, blank=True)    # End date of the payment period

    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField(max_length=100,null=True, blank=True)
    payment_receipt = models.FileField(upload_to='salary_receipts/', null=True, blank=True)

    @property
    def get_payment_history(self):
        if self.salarypaymenthistory_set.all():
            return self.salarypaymenthistory_set.all()
        return None
    
    @property
    def get_payment_method(self):
        if self.payment_method:
            return self.payment_method.name
        return None
    

    @property
    def get_total_amount(self):
        if self.payment_amount:
            return get_amount_or_zero(self.payment_amount)
        return 0
    


    @property
    def get_pending_amount(self):
        # if  self.get_payment_history:
        #     amount = sum(i.get_amount_paid for i in self.get_payment_history)
            # total_amount =get_amount_or_zero(self.amount_paid)
        #     ret = total_amount - amount 
        #     return ret if ret >=0 else 0 
        if self.get_paid_amount:
            total_amount =self.get_total_amount
            ret = total_amount - self.get_paid_amount
            return ret if ret >=0 else 0 
        return self.amount_paid
    

    @property
    def get_paid_amount(self):
        if  self.get_payment_history:
            amount = sum(i.get_amount_paid for i in self.get_payment_history)
            return amount
        return 0
        # return self.amount_paid
    

    @property
    def is_paid(self):
        if self.get_pending_amount <=0:
            return True
        return False



class SalaryPaymentHistory(models.Model):
    receipt = models.ForeignKey(SalaryReceipt, on_delete=models.CASCADE, null=True, blank=True)
    created_by=models.ForeignKey(Employee,null=True,blank=True, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField(max_length=100,null=True, blank=True)
    payment_receipt = models.FileField(upload_to='salary_receipts/', null=True, blank=True)



    @property
    def get_salary_receipt(self):
        if self.receipt:
            return self.receipt
        return None
        
    @property
    def get_pending(self):
        if self.get_salary_receipt and self.get_salary_receipt.get_payment_history:
            amount = sum(i.get_amount_paid for i in self.get_salary_receipt.get_payment_history )
            total_amount =get_amount_or_zero(self.get_salary_receipt.amount_paid)
            ret = total_amount - amount 
            return ret if ret >=0 else 0
        return 0

   
    @property
    def get_amount_paid(self):
        return get_amount_or_zero(self.amount_paid)
    

    @property
    def get_payment_method(self):
        if self.payment_method:
            return self.payment_method.name
        return None


# --------------------------------------------------------------- Project Sub Contracct -----------------------------------------------------------------

# make acontract for project
class ProjectSubContract(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    name= models.CharField(max_length=255,null=True,blank=True)
    type = models.ForeignKey(ContractType, on_delete=models.CASCADE,null=True,blank=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE,null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    contract_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_schedule = models.ForeignKey(PaymentSchedule, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(WorkStatus, on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField() 
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    terms_conditions = models.TextField()
    created_at= models.DateField(auto_now_add=True)
    created_by=models.ForeignKey(Employee,null=True,blank=True, on_delete=models.CASCADE)
   
    def save(self, *args, **kwargs):
        if not self.pk: 
            default_status = WorkStatus.objects.filter(code="-2").last()
            if default_status:
                self.status = default_status
        super().save(*args, **kwargs)

    

    @property
    def display(self):
        if self.project :
            return self.project.proj_name
        return "unnamed"
    
    @property
    def display_contractor(self):
        if self.contractor :
            return self.contractor.name
        return "unnamed"
    

    @property
    def display_contractor_dropdown(self):
       return self.display + "-->" + self.display_contractor
    

#    @property
#    def display_contractor_dropdown(self):
#         contractors = self.contractor_set.all()  
#         if not contractors:
#             return self.contractor_name
#         return ", ".join(contractor.name for contractor in contractors)

#     def __str__(self):

# @property
# def display_contractor_dropdown(self):
#         return self.contractor.name

#     def __str__(self):
#         return f"{self.project.name} - {self.contractor.name} - {self.contract_amount}"




    
    # @property
    # def get_contract_invoice(self):
    #     return self.get_contract_invoice

    @property
    def get_service_rates(self):
        if self.projectsubcontractunitrates_set.all():
            return self.projectsubcontractunitrates_set.all()
        return None
    
    @property
    def get_labour_rates(self): #ProjectSubContractLabourWages
        if self.projectsubcontractlabourwages:
            return self.projectsubcontractlabourwages
        return None
    

    @property
    def get_labour_attendence(self):
        if self.projectsubcontractlabourattendence_set.all():
            return self.projectsubcontractlabourattendence_set.all()
        return None
    

    @property
    def get_today_attendence(self):
        today =get_today()
        if self.get_labour_attendence:
            return self.get_labour_attendence.filter(date=today).last()
        return None
    

    @property
    def get_contract_invoice(self):
        if self.contractorinvoice_set.all():
            return self.contractorinvoice_set.all()
        return None
    

    @property
    def get_pending_amount(self):
        contract_invoices = self.get_contract_invoice
        if contract_invoices:
            total_paid_amount = sum(invoice.get_paid_amount for invoice in contract_invoices)

            pending_amount = self.get_contract_amount - total_paid_amount
            return pending_amount if pending_amount > 0 else 0
        
        return self.get_contract_amount
    

    @property
    def get_contract_amount(self):
        if self.contract_amount:
            return self.total_service_amount if self.total_service_amount else self.contract_amount
        return None
    


    @property
    def get_paid_amount(self):
        contract_invoices = self.get_contract_invoice
        if contract_invoices:
            total_paid_amount = sum(invoice.get_paid_amount for invoice in contract_invoices)
            return total_paid_amount
        return None
       
    

    @property
    def total_service_amount(self):
        service_rates= self.get_service_rates
        if service_rates :
            total_amount = sum(rate.get_total for rate in service_rates)
            return total_amount
        return None
    


    @property
    def is_contract_invoiced(self):
        contract_invoices = self.get_contract_invoice
        if contract_invoices:
            total_amount = sum(invoice.amount for invoice in contract_invoices)
            if total_amount >= self.get_contract_amount  :
                return  True
        return False
    

    @property
    def pending_invoice_amount(self):
        contract_invoices = self.get_contract_invoice
        if contract_invoices:
            total_amount = sum(invoice.get_invoice_amount for invoice in contract_invoices)
            total_amount = self.get_contract_amount - total_amount 
            return  total_amount 
        return self.get_contract_amount


    @property
    def paid_status(self):
        pending= self.get_pending_amount
        if self.is_contract_invoiced:
            return self.is_contract_invoiced
        # if pending :
        #     return False
        return False
        
    

    @property
    def total_wages(self):
        labour_wages = self.projectsubcontractlabourwages

        if self.get_labour_attendence :
            total_wages = (
                self.get_labour_attendence.aggregate(
                    maistry=Sum('maistry') * labour_wages.maistry ,
                    maison_cooli=Sum('maison_cooli')  * labour_wages.maison_cooli,
                    male_skilled=Sum('male_skilled') * labour_wages.male_skilled,
                    male_unskilled=Sum('male_unskilled') * labour_wages.male_unskilled,
                    female_skilled=Sum('female_skilled') * labour_wages.female_skilled,
                    female_unskilled=Sum('female_unskilled') * labour_wages.female_unskilled,

                    maistry_ot=Sum('maistry_ot') * (labour_wages.maistry / DUTY_HOURS),
                    maison_cooli_ot=Sum('maison_cooli_ot') * (labour_wages.maison_cooli /DUTY_HOURS ),
                    male_skilled_ot=Sum('male_skilled_ot') * (labour_wages.male_skilled / DUTY_HOURS) ,
                    male_unskilled_ot=Sum('male_unskilled_ot') * (labour_wages.male_unskilled / DUTY_HOURS),
                    female_skilled_ot=Sum('female_skilled_ot') * (labour_wages.female_skilled / DUTY_HOURS ),
                    female_unskilled_ot=Sum('female_unskilled_ot') *( labour_wages.female_unskilled /DUTY_HOURS )
                )
            )
            total_wages = {key: value if value is not None else Decimal(0) for key, value in total_wages.items()}
            print(total_wages)

            # Perform the sum of Decimal values
            total_wages_sum = sum(total_wages.values())
            return total_wages_sum
        return Decimal(0)

    

    # @property
    # def get_today_attendence(self):
    #     maistry =0,
    #     maison_cooli =0 
    #     attendence_data  = { "male_skilled": "0",
    #         "male_unskilled": "0",
    #         "female_skilled": "0",
    #         "female_unskilled": "0",
    #         "maistry_ot": "0",
    #         "maison_cooli_ot": "0",
    #         "male_skilled_ot": "0",
    #         "male_unskilled_ot": "0",
    #         "female_skilled_ot": "0",
    #         "female_unskilled_ot": "0",
    #         "company": None,
    #         "created_by": None,
    #         "contract": None,
    #          "atten_id" : 0
    #         }
    #     project = None
    #     atten_id =  0
    #     today =get_today()
     
    #     if self.get_labour_attendence.exists():
    #         today =self.get_labour_attendence.filter(date=today).last()
    #         print(today,"today")
    #         if today:
    #            maistry =today.maistry
    #            maison_cooli =today.maison_cooli
    #            attendence_data = { "male_skilled": today.male_skilled,
    #                 "male_unskilled": today.male_unskilled,
    #                 "female_skilled": today.female_skilled,
    #                 "female_unskilled":today.female_unskilled,
    #                 "maistry_ot": today.maistry_ot,
    #                 "maison_cooli_ot":today.maison_cooli_ot,
    #                 "male_skilled_ot": today.male_skilled_ot,
    #                 "male_unskilled_ot":today.male_unskilled_ot,
    #                 "female_skilled_ot":today.female_skilled_ot,
    #                 "female_unskilled_ot":today.female_unskilled_ot,
    #                 # "company": today.company,
    #                 "created_by": today.created_by,
    #                 "contract": today.contract,
    #               "atten_id" :today.id
    #                 }
                
    #     return attendence_data

    
# ITEM RATES
class ProjectSubContractUnitRates(models.Model):
    contract = models.ForeignKey(ProjectSubContract, on_delete=models.CASCADE, null=True, blank=True)
    created_by=models.ForeignKey(Employee,null=True,blank=True, on_delete=models.CASCADE)
    work =models.TextField() 
    unit= models.ForeignKey(Uom, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount= models.DecimalField(max_digits=10, decimal_places=2, default=0)


    @property
    def get_total(self):
        if self.rate and self.total_qty:
            return self.rate * self.total_qty
        return 0

# wages amount
class ProjectSubContractLabourWages(models.Model):
    contract = models.OneToOneField(ProjectSubContract, on_delete=models.CASCADE, null=True, blank=True)
    created_by=models.ForeignKey(Employee,null=True,blank=True, on_delete=models.CASCADE)
    maistry = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    maison_cooli = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    male_skilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    male_unskilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    female_skilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    female_unskilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date=models.DateField(auto_now_add=True)

# contract labours  app
class ProjectSubContractLabourAttendence(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)#---- added new ----
    created_by=models.ForeignKey(Employee,null=True,blank=True, on_delete=models.CASCADE)
    contract = models.ForeignKey(ProjectSubContract, on_delete=models.CASCADE, null=True, blank=True)
    maistry = models.DecimalField(max_digits=10, decimal_places=2, default=0.0,null=True,blank=True)
    maison_cooli = models.DecimalField(max_digits=10, decimal_places=2, default=0.0,null=True,blank=True)
    male_skilled = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    male_unskilled = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    female_skilled = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    female_unskilled = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    maistry_ot = models.DecimalField(max_digits=10, decimal_places=2, default=0.0,null=True,blank=True)
    maison_cooli_ot = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    male_skilled_ot = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    male_unskilled_ot = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    female_skilled_ot = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    female_unskilled_ot = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    date=models.DateField(null=True, blank=True)


# make invoice for project
class ContractorInvoice(models.Model):
    created_by=models.ForeignKey(Employee,null=True,blank=True, on_delete=models.CASCADE)
    contract = models.ForeignKey(ProjectSubContract, on_delete=models.CASCADE, null=True, blank=True)
    invoice_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True, blank=True)
    payment_due_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE, null=True, blank=True)
    invoice_number = models.CharField(max_length=100,null=True, blank=True)  
    terms_conditions = models.TextField(null=True,blank=True)
    documents = models.FileField(upload_to='invoices/', null=True, blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField(max_length=100,null=True, blank=True)   

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    @property
    def get_status(self):
        if self.status:
            return self.status.name
        return None    

    def update_status(self):
        print('enterrrrrrrrrrr')
        
        if self.get_paid_amount == self.amount :
            self.status =PaymentStatus.objects.filter(code = 0).last()
        elif self.get_paid_amount ==0:
            self.status =PaymentStatus.objects.filter(code = -1).last() 
        else :
            self.status =PaymentStatus.objects.filter(code = 1).last() 
        
        self.pending_amount =self.amount -self.paid_amount
        self.save()    

    @property
    def get_payment_history(self):
        if self.contractorinvoicepaymenthistory_set.all():
            return self.contractorinvoicepaymenthistory_set.all()
        return None

    @property
    def get_paid_amount(self):
        pay_history= self.get_payment_history
        if pay_history:
            total_amount = sum(i.amount_paid for i in pay_history)
            return  total_amount
        return 0    

    @property
    def get_invoice_amount(self):
        if self.amount:
            return self.amount
        return 0    

    @property
    def is_invoice_paid(self):
        pay_history= self.get_payment_history
        if pay_history:
            total_amount = sum(i.amount_paid for i in pay_history)
            if total_amount >= self.get_invoice_amount  :
                return  True
        return False    

    @property
    def get_pending_amount(self):
        pay_history= self.get_payment_history
        if pay_history:
            total_amount = sum(i.amount_paid for i in pay_history)
            total_amount = self.get_invoice_amount - total_amount 
            return  total_amount
        return self.get_invoice_amount    

# make payment receipt
class ContractorInvoicePaymentHistory(models.Model):
    invoice = models.ForeignKey(ContractorInvoice, on_delete=models.CASCADE, null=True, blank=True)
    created_by=models.ForeignKey(Employee,null=True,blank=True, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField(max_length=100,null=True,blank=True)
    payment_receipt = models.FileField(upload_to='payment_receipts/', null=True, blank=True)

    def save(self, *args, **kwargs):
        data =super().save(*args, **kwargs)
        if self.invoice:
            invoice =self.invoice
            invoice.update_status()
        return data



# ------------------------------------------------------------ attendence mangment   -------------------------------------

# company staff labour attendance
class ProjectLabourAttendence(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    labour = models.ForeignKey(CompanyLabours, on_delete=models.CASCADE, null=True, blank=True)
    over_time = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)
    clock_in=models.TimeField(null=True, blank=True)
    clock_out=models.TimeField(null=True, blank=True)
    date=models.DateField(null=True,blank=True)
    present=models.BooleanField(default=False)
    wage = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)


    class Meta:
        constraints = [
            UniqueConstraint(fields=['labour', 'date'], name='unique_labour_date')
        ]


    def save(self, *args, **kwargs):
        if not self.date:
            self.date = today_date
        if self.clock_in:
            self.present =True
            if self.labour :
                self.wage = self.labour.get_rate 
        return super().save(*args, **kwargs)
    
    @property
    def get_wage(self):
        amount =0
        if self.wage and self.present and self.clock_in:
            amount+= get_amount_or_zero(self.wage)
            if self.over_time:
                ot= get_amount_or_zero(self.wage)/DUTY_HOURS
                amount+= get_amount_or_zero(self.over_time)*ot
        return amount

# employee attendence
class Attendance(models.Model):
    clock_in=models.TimeField(null=True, blank=True)
    clock_out=models.TimeField(null=True, blank=True)
    employee=models.ForeignKey(Employee,null=True,blank=True, on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True,null=True,blank=True)
    present=models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    over_time = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)
    wage = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)

    class Meta:
       ordering = ['-pk'] 

    class Meta:
        unique_together = ('employee', 'date')

    def save(self, *args, **kwargs):
        if self.clock_in:
            self.present =True
            if self.employee :
                self.wage = (self.employee.get_daily_wage )
        return super().save(*args, **kwargs)

    @property
    def employee_info(self):
        if self.employee:
            return self.employee
        return 
    
    def in_time(self):
        if self.clock_in:
            return self.clock_in.strftime('%I:%M %p')  # Format with AM/PM
        else:
            return ""
    
    def out_time(self):
        if self.clock_out:
            return self.clock_out.strftime('%I:%M %p')  # Format with AM/PM
        else:
            return ""
        
    @property
    def get_wage(self):
        amount =0
        if self.wage and self.present and self.clock_in:
            print(get_amount_or_zero(self.wage))
            amount+= get_amount_or_zero(self.wage)
            if self.over_time:
                ot= get_amount_or_zero(self.wage)/DUTY_HOURS
                amount+= get_amount_or_zero(self.over_time)*ot
        return amount

# ----------------------------------------------------  --------------------------------------------------------------------------------



# ------------------------ PROJECT  expense --------------------------------------------------- ---------------------

class Expense(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    particular = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    site_location = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True ) 
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True) 
    attachment  =models.FileField(upload_to="doc",null=True, blank=True)

# machinary works
class ProjectMachineExpense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    machine = models.ForeignKey(CompanyMachinaryCharges, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    payment_schedule =  models.ForeignKey(PaymentSchedule, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    attachment  =models.FileField(upload_to="doc",null=True, blank=True)




class Files(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    project_name =  models.ForeignKey(Project,on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='file/', null=True, blank=True)


class EmployeeProfile(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_profile')
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.employee.name}"
    
class CompanyProfile(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.company.name} Profile"
    

class PettyCash(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    particular = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    site_location = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True ) 
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True) 
    attachment  =models.FileField(upload_to="doc")




class PaymentHistory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    img =models.FileField(upload_to="doc",null=True,blank=True)
    receipt_number = models.CharField(max_length=100)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

class DailySiteStockUsage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    stock=models.ForeignKey(SiteStock,on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    subcontract=models.ForeignKey(ProjectSubContract,on_delete=models.CASCADE, null=True, blank=True)
    # work_done=models.TextField()
    date = models.DateField(auto_now_add=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    unit = models.ForeignKey(Uom,on_delete=models.CASCADE,null=True,blank=True)

# @property
#   def get_dailysitestockusage_items(self):
#         if self.dailysitestockusageitems_set.all():
#             return self.dailysitestockusageitems_set.all()
#         return None

class Dailytask(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    subcontract=models.ForeignKey(ProjectSubContract,on_delete=models.CASCADE, null=True, blank=True)
    # subcontract_items=models.ForeignKey(ProjectSubContractUnitRates,on_delete=models.CASCADE, null=True, blank=True)
    work_done=models.TextField()
    date=models.DateField(auto_now_add=True)
    qty=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    unit=models.ForeignKey(Uom, on_delete=models.CASCADE, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if self.stock:
    #         stock =self.stock
    #         stock.qty -=self.qty
    #         stock.save() 
    #     return  super().save(*args, **kwargs)

  


class SiteAllocation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True,blank=True)
    labour = models.ForeignKey(CompanyLabours, on_delete=models.CASCADE, null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    
    @property
    def get_date(self):
        if self.date:
            return self.date
        return "sdfsdf"

