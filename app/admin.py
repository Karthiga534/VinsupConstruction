from .models import *
from django.contrib import admin

#------------------------------------------------------------------------------- Dharshini ---------------------------------------------------------

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name','email',"phone_number")
    search_fields = ['username', 'email']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','admin',)

@admin.register(Uom)
class UomAdmin(admin.ModelAdmin):
    list_display = ('name','company')

@admin.register(EmpRoles)
class EmpRolesAdmin(admin.ModelAdmin):
    list_display = ('company','name','description',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('company','name','role',)

@admin.register(VendorRegistration)
class VendorRegistrationAdmin(admin.ModelAdmin):
    list_display = ('company','vendorname','companyname','gstno','mobile','email','faxno','address')

@admin.register(VendorQuatation)
class VendorQuatationAdmin(admin.ModelAdmin):
    list_display = ('company','vendorname')

@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display = ( 'company', 'vendor')

admin.site.register(PurchaseItems)

admin.site.register(Quatation)

@admin.register(QuatationItems)
class QuatationItemsAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','company')

admin.site.register(SiteStock)

@admin.register(TransferInvoice)
class TransferInvoiceAdmin(admin.ModelAdmin):
    list_display = ['id']
# admin.site.register(TransferItems)

@admin.register(TransferItems)
class TransferItemsAdmin(admin.ModelAdmin):
    list_display =[ 'id']

@admin.register(DailySiteStockUsage)
class DailySiteStockUsageAdmin(admin.ModelAdmin):
    list_display =[ 'id']

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Contractcategory)
class ContractCategoryAdmin(admin.ModelAdmin):
    list_display = ('id',)




#------------------------------------------------------------------------------- End  Dharshini ---------------------------------------------------------


admin.site.register(Project)
admin.site.register(MaterialLibrary)
admin.site.register(Priority)
admin.site.register(Duration)
admin.site.register(InventoryStock)


admin.site.register(ProjectSubContract)
admin.site.register(ProjectSubContractUnitRates)
admin.site.register(ProjectSubContractLabourWages)




@admin.register(ProjectSubContractLabourAttendence)
class ProjectSubContractLabourAttendenceAdmin(admin.ModelAdmin):
     list_display = ('id',)


admin.site.register(ContractorInvoice)
admin.site.register(ContractType)
admin.site.register(PaymentSchedule)
admin.site.register(WorkStatus)
admin.site.register(PaymentMethod)
# admin.site.register(Expense)


admin.site.register(PaymentStatus)
admin.site.register(ContractorInvoicePaymentHistory)



# admin.site.register(TransferInvoice)
# admin.site.register(TransferItems)

@admin.register(CompanyMachinaryCharges)
class CompanyMachinaryChargesAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'payment_schedule')


@admin.register(LabourRolesAndSalary)
class LabourRolesAndSalaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'payment_schedule')


@admin.register(CompanyLabours)
class CompanyLaboursAdmin(admin.ModelAdmin):
    list_display = ('name',)  


@admin.register(ProjectLabourAttendence)
class ProjectLabourAttendenceAdmin(admin.ModelAdmin):
     list_display = ('id','date',)

admin.site.register(OTP)
admin.site.register(Salary)
admin.site.register(SalaryReceipt)
admin.site.register(SalaryPaymentHistory)
admin.site.register(Attendance)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id',)  

@admin.register(Dailytask)
class DailytaskAdmin(admin.ModelAdmin):
    list_display = ('id',)  

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('id','project_name','file',)

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(ProjectMachineExpense)

admin.site.register(DailyMaterialUsage)

@admin.register(PettyCash)
class PettyCashAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(PaymentHistory)

admin.site.register(SiteAllocation)

# @admin.register(SiteAllocation)
# class SiteAllocationAdmin(admin.ModelAdmin):
#     list_display = ('id','date',)