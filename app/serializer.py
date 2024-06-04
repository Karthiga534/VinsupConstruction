import string
import random
from .models import *
from decimal import Decimal
from django.conf import settings
from app.auth_models import Company
# from .models import Purchase
from rest_framework import serializers
from rest_framework.serializers import *
from django.contrib.auth.hashers import make_password
from .models import PurchaseItems, MaterialLibrary, InventoryStock



#-------------------------------------------------------------------- Dharshini ----------------------------------------------------------------

date_format = "%Y-%m-%d"
# date_format =settings.DATE_FORMAT



class UomSerializer(ModelSerializer):

    class Meta:
        model = Uom
        fields = "__all__"
        #fields = ("id","name")

class VendorRegistrationSerializer(ModelSerializer):
    class Meta:
        model = VendorRegistration
        fields = "__all__"

class VendorQuatationSerializer(ModelSerializer):
    class Meta:
        model = VendorQuatation
        fields = "__all__"

class PurchaseInvoiceSerializer(ModelSerializer):
    class Meta:
        model = PurchaseInvoice
        fields = "__all__"


    def validate_invoice_id(self, attrs):
        company = self.initial_data.get('company')
        if PurchaseInvoice.objects.filter(invoice_id=attrs, company=company).exists():
            raise ValidationError ('Already exists')
        return super().validate(attrs)
    

    # def validate_created_at(self, value):
    #     print('Created At Validation')
    #     try:
    #         # Attempt to parse the date
    #         parsed_date = datetime.strptime(value, '%Y-%m-%d')  # Adjust format as needed
    #     except ValueError:
    #         raise ValidationError("Invalid date format. Expected format is YYYY-MM-DD.")
    #     return parsed_date.date() 


    
    def run_validation(self, data=serializers.empty):
        try:
            return super().run_validation(data)
        except serializers.ValidationError as e:
            # Check if the error message is due to uniqueness constraint
            if 'invoice_id' in e.detail and 'company' in e.detail:
                error_msg = {'invoice_id': ['An invoice with this ID already exists for this company.']}
                e.detail = error_msg

            if 'created_at' in e.detail :
                error_msg = {'created_at': ['Invalid Date.']}
                e.detail = error_msg
            raise e
        







from decimal import Decimal
from django.db.models import F

class   PurchaseItemsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, allow_blank=True, required=False)
    company  = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(),required=False,write_only=True)

    class Meta:
        model = PurchaseItems
        fields = '__all__'

    def create(self, validated_data):
        site = self.context.get('site')

        item = validated_data.get('item' ,None)
        # Extract unit and price from validated data
        # price = validated_data.pop('price', 0) 
        if not item:
            mlib={}
            # mlib['item'] =validated_data.get("name",None)
            # mlib['price'] = validated_data.get('price',None)
            # mlib ['company'] =validated_data.get('company',None)
            # mlib ['unit']=validated_data.get('unit',None)
            # item = MaterialLibrary.objects.create(**mlib)
            name = validated_data.get("name", None)
            print(item)
            price = validated_data.get('price', None)
            company = validated_data.get('company', None)
            unit = validated_data.get('unit', None)
            item =MaterialLibrary.objects.filter(item__iexact =name,company=company,unit=unit).last()
            if not item:
                item =MaterialLibrary.objects.create(item=name,company=company,unit=unit,price = price, )
  
        unit = validated_data.pop('unit', None)
        company=validated_data.pop('company')
        qty_to_add = Decimal(validated_data.get('qty', 0))
        sub_total = Decimal(validated_data.get('sub_total', 0))
        

        
            # Check if the item exists in InventoryStock
        inventory_item, inventory_created = InventoryStock.objects.get_or_create(item = item,unit=unit,company=company)

        # if site  is there set item purchased for particular site so no need to manipulate inventory stock
        inventory_item.qty = ( 0 if site else Decimal(inventory_item.qty)) + qty_to_add
        if not inventory_item.price:
            inventory_item.price =  Decimal(validated_data.get('price', 0))
        inventory_item.total_amount = inventory_item.qty * inventory_item.price
        inventory_item.save()
        
        # else:
        #     inventory_created.qty = Decimal(inventory_created.qty) + qty_to_add
        #     inventory_created.price = Decimal(validated_data.get('price', 0))
        #     inventory_created.total_amount = sub_total
        #     inventory_created.save()

        if site:
             validated_data['for_site']  = True
        # validated_data['name'] = item_name  # Add 'name' field to validated_data
        validated_data['unit'] = unit  # Add 'unit' field to validated_data
        validated_data['item'] = item
       
        validated_data['inventory'] = inventory_item
        purchase_item = super().create(validated_data)  # Create PurchaseItems instance
        
        return purchase_item
    


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["item_name"] = instance.item.item if instance.item else None
        data ['unit_name'] = instance.unit.name if instance.unit else None
        return data




class PurchaseInvoiceListSerializer(ModelSerializer):
    get_purchase_items =PurchaseItemsSerializer(many=True,read_only=True)
    class Meta:
        model = PurchaseInvoice
        fields = "__all__"


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["vendor_name"] = instance.vendor.display if instance.vendor else None
        # data ['unit_name'] = instance.unit.name if instance.unit else None
        return data

class QuatationItemsSerializer(ModelSerializer):
    class Meta:
        model = QuatationItems
        fields = "__all__"

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["item_name"] = instance.display_name
        data ['unit_name'] = instance.unit.name if instance.unit else None
        return data
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)

    #     invoice = instance.invoice
    #     inventory = instance.inventory
    #     unit = instance.unit

    #     invoice_representation = None
    #     inventory_representation = None
    #     unit_representation = None

    #     if invoice:
    #         invoice_representation = {
    #             'id': invoice.id,
    #             'name': invoice.site.site_location  
    #         }
        
    #     if inventory:
    #         inventory_representation = {
    #             'id': inventory.id,
    #             'name': inventory.item.item
    #         }
        
    #     if unit:
    #         unit_representation = {
    #             'id': unit.id,
    #             'name': unit.name 
    #         }

    #     representation['invoice'] = invoice_representation
    #     representation['inventory'] = inventory_representation
    #     representation['unit'] = unit_representation

    #     return representation

class QuatationSerializer(ModelSerializer):



    class Meta:
        model = Quatation
        fields = "__all__"



   




class QuatationListSerializer(ModelSerializer):
    get_quotation_items =QuatationItemsSerializer(many=True,read_only=True)
    class Meta:
        model = Quatation
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["site_name"] = instance.site.display if instance.site else None
        return data




class EmpRolesSerializer(ModelSerializer):
    class Meta:
        model = EmpRoles
        fields = "__all__"

class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


    # def validate_mobile(self, attrs):
    #     if Employee.objects.filter(mobile=attrs).exists():
    #         raise ValidationError ('already exists')
    #     if CustomUser.objects.filter(phone_number=attrs).exists():
    #         raise ValidationError ('Already exists')
    #     return super().validate(attrs)

    def create(self, validated_data):
        user_data={}
        user_data["pin"] = get_pin()
        user_data["phone_number"] = validated_data.get('mobile', None) 
        user_data["name"] = validated_data.get('name', None) 

        password =get_password(user_data["name"])
        user_data["password"]=  make_password(password) 

        print(password)
        phone=user_data["phone_number"]
        user = CustomUser.objects.create(**user_data)
        # user.is_employee=True
        # user.save()
        # msg=""
        # send_sms=""
        validated_data["user"] =user    
        employee = super().create(validated_data)
        return employee

def get_pin():
    pin = ''.join([str(random.randint(0, 9)) for _ in range(4)])  
    return pin


def get_password(name):
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) 
    return password
    

class TransferItemsListSerializer(ModelSerializer):

    class Meta:
        model = TransferItems
        fields = "__all__"

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.item:
            data ['item_name'] = instance.name if instance.name else instance.item.item
            data ['item_unit'] = instance.unit.name if instance.unit else instance.item.unit.name
        else:
            data ['item_name'] = instance.name if instance.name else None
            data ['item_unit'] = instance.unit.name if instance.unit else None
        return data


class TransferInvoiceSerializer(ModelSerializer):
    get_transfer_items =TransferItemsListSerializer(many=True,read_only=True)
    # from_site= serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = TransferInvoice
        fields = "__all__"

    # def get_items(self,instance):
    #     return instance.get_transfer_items


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ['from_site'] = instance.from_site.site_location if instance.from_site else None
        data ['from_inventory'] = instance.from_inventory.name if instance.from_inventory else None
        data ['to_site'] = instance.to_site.site_location if instance.to_site else None
        data ['to_inventory'] = instance.to_inventory.name if instance.to_inventory else None
        return data

class TransferItemsSerializer(ModelSerializer):
    stock_id =serializers.CharField(required=False,write_only=True)

    class Meta:
        model = TransferItems
        fields = "__all__"




    def create(self, validated_data):
        invoice =validated_data.get('invoice')
        qty = validated_data.get('qty')
        item = validated_data.get('item')
        # unit = validated_data.get('unit')

    
        stock_id = validated_data.pop('stock_id')

        try :
            source = get_source_stock(invoice, stock_id)
            # if invoice.from_site:
            #     # source= invoice.from_site.stock
            #     source= SiteStock.objects.filter(id=stock_id).last()
                
            # if invoice.from_inventory :
            #     source= InventoryStock.objects.filter(id=stock_id).last()
            #     # source= invoice.from_inventory.stock
        except:
            return ValidationError('Source not found')
        

         # site data
        site_data=validated_data.copy()
        site_data.pop('invoice')
        site_data['name'] =item.item
        site_data['company'] =invoice.company
        site_data['unit'] =source.unit
        
        if invoice.to_site:
            if not invoice.to_site.stock :
                # site_data.pop('invoice')
                site_data['project'] =invoice.to_site

                # site_data['name'] =item.item
                # site_data['company'] =invoice.company
                # site_data['unit'] =source.unit
                SiteStock.objects.create(**site_data)

            destiny= invoice.to_site.stock

            destiny_obj = destiny.filter(item = item).last()
            if not destiny_obj:
                # site_data=validated_data.copy()
                # site_data.pop('invoice')
                site_data['project'] =invoice.to_site

                # site_data['name'] =item.item
                # site_data['company'] =invoice.company
                # site_data['unit'] =source.unit
                SiteStock.objects.create(**site_data)

          
        if invoice.to_inventory :
            destiny = invoice.to_inventory.stock 
            if not invoice.to_inventory.stock :
                # site_data=validated_data.copy()
                # site_data.pop('invoice')
                # site_data['company'] =invoice.company
                # site_data['name'] =item.item
                # site_data['unit'] =source.unit
                InventoryStock.objects.create(**site_data)
                
            # destiny= invoice.to_inventory.stock


            destiny_obj = destiny.filter(item = item).last()

            if not destiny_obj:
                # site_data=validated_data.copy()
                # site_data.pop('invoice')
                # site_data['company'] =invoice.company
                # site_data['name'] =item.item
                # site_data['unit'] =source.unit
                InventoryStock.objects.create(**site_data)

        if source and destiny :
            # source = source.filter(item = item,unit=unit).last()   #use id
            source.qty =Decimal(source.qty) - Decimal(qty)
            source.save()

            destiny = destiny.filter(item = item).last()  #useid
            if destiny :
                destiny.qty = Decimal(destiny.qty) + Decimal(qty)
                destiny.total_supplied_qty = Decimal(destiny.total_supplied_qty) + Decimal(qty)
                destiny.save()

        validated_data['name'] =item.item
        validated_data['unit'] =source.unit  
        return super().create(validated_data)
        

    
    # def create(self, validated_data):
    #     instance =validated_data.get('invoice')
    #     qty = validated_data.get('qty')
    #     item = validated_data.get('item')
    #     # unit = validated_data.get('unit')
    #     site_data=validated_data.copy()
    #     site_data.pop('invoice')

    #     stock_id = validated_data.pop('stock_id')

    #     try :
    #         source = get_source_stock(instance, stock_id)

    #         if instance.to_site:
    #             destiny = instance.to_site.stock.filter(item=item).last()
    #         if not destiny:
    #             destiny = create_site_stock({
    #                 'project': instance.to_site,
    #                 'name': item.item,
    #                 'company': instance.to_site.company,
    #                 'unit': source.unit if source else None,
    #                 'item' :item
    #             })

    #         elif instance.to_inventory:
    #             destiny = instance.to_inventory.stock.filter(item=item).last()
    #         if not destiny:
    #             destiny = create_inventory_stock({
    #                 'company': instance.to_site.company,
    #                 'name': item.item,
    #                 'unit': source.unit if source else None,  
    #                 'item' :item  # Assuming source has a unit attribute
    #             })

    #         qty = Decimal(item.qty)
    #         if source and destiny:
    #             update_stock_qty(source, qty)
    #             update_destiny_qty(destiny, qty)

    #     except Exception as e:
    #         return ValidationError('Item not found')

    #     return super().create(validated_data)
        
def get_source_stock(invoice, stock_id):
    if invoice.from_site:
        return SiteStock.objects.filter(id=stock_id).last()
    elif invoice.from_inventory:
        return InventoryStock.objects.filter(id=stock_id).last()
    else:
        raise ValidationError('Source not specified')

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


#------ Project Sub Category ------ new  



class DailySiteStockUsageSerializer(ModelSerializer):
    

    class Meta:
        model = DailySiteStockUsage
        fields = "__all__"
    
class ProjectSubContractSerializer(ModelSerializer):
    class Meta:
        model = ProjectSubContract
        fields = "__all__"

class ProjectSubContractUnitRatesSerializer(ModelSerializer):
    class Meta:
        model = ProjectSubContractUnitRates
        fields = "__all__"

class ProjectSubContractLabourWagesSerializer(ModelSerializer):
    class Meta:
        model =ProjectSubContractLabourWages
        fields= "__all__"


#-------------------------------------------------------------------- End Dharshini ----------------------------------------------------------------

class ContractcategorySerializer(ModelSerializer):
    class Meta:
        model = Contractcategory
        fields = '__all__'

class ContractorSerializer(ModelSerializer):
    class Meta:
        model = Contractor
        fields = '__all__'


class ProjectCategorySerializer(ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'


class MaterialLibrarySerializer(ModelSerializer):
    class Meta:
        model = MaterialLibrary
        fields = '__all__'


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # proj_category = instance.proj_category
        # status = instance.status
        # data ={}
        data['id'] =instance.id
        data ["proj_name"] =  instance.proj_name
        data ["site_location"] = instance.site_location
        data ["start_date"] = instance.start_date

        data["proj_category"] = instance.proj_category.name   if instance.proj_category else None
        
        data ['status_name'] =  instance.status.name if instance.status else None

        return data



#-------------- New ---------------        

class CompanyMachinaryChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMachinaryCharges
        fields = "__all__"


class LabourRolesAndSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LabourRolesAndSalary
        fields = "__all__"
        
class CompanyLaboursSerializer(serializers.ModelSerializer):
    # company_rate = serializers.BooleanField(required=False)
    class Meta:
        model = CompanyLabours
        fields = '__all__'
        # fields = ['name', 'role', 'company_rate', 'rate', 'ot_rate', 'payment_schedule']

    # def update(self, instance, validated_data):
    #     print()
    #     print(validated_data,"validated data")
    #     return super().update(instance, validated_data)

class ExpenseSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField()

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'attachment', 'company', 'date', 'employee', 'particular', 'site_location'] 

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ['employee_name'] =instance.employee.name if instance.employee else None
        data ['site_name'] =instance.site_location.display if instance.site_location else None
        return data 


class SiteStockSerializer(ModelSerializer):
    unit = serializers.SerializerMethodField(read_only=True)
    item = MaterialLibrarySerializer(read_only=True)
    get_total =serializers.CharField(read_only=True)

    class Meta:
        model = SiteStock
        fields = '__all__'

    def get_unit(self, obj):
        unit_obj = obj.unit
        if unit_obj is not None:
            return unit_obj.name
        return None
    
class InventoryStockSerializer(ModelSerializer):
    unit = serializers.SerializerMethodField()
    item = MaterialLibrarySerializer()
    get_total =serializers.CharField(read_only=True)

    class Meta:
        model = InventoryStock
        fields = '__all__'

    def get_unit(self, obj):
        unit_obj = obj.unit
        if unit_obj is not None:
            return unit_obj.name
        return None
    


# -------------------------------- contractor -payment -------------------------------------------

class ContractInvoiceHistorySerializer(ModelSerializer):
    class Meta:
        model = ContractorInvoicePaymentHistory
        fields = ('id',"payment_date",'amount_paid','transaction_id','invoice','payment_method')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["payment_method"] =instance.payment_method.name if instance.payment_method else None
        return data
    
    def create(self, validated_data):
        # invoice = validated_data.get('invoice',None)
        # invoice.update_status()
        return super().create(validated_data)

class ContractorInvoiceSerializer(ModelSerializer):
    get_payment_history = ContractInvoiceHistorySerializer(many=True,read_only=True)

    class Meta:
        model = ContractorInvoice
        fields = ('id',"get_payment_history",'invoice_date','amount','paid_amount','invoice_number','from_date','to_date','payment_method','contract')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["payment_method"] =instance.payment_method.name if instance.payment_method else None
        data ["status"] =instance.get_status
        data ["status_code"] =instance.status.code if instance.status else None
        data ["get_paid_amount"] =instance.get_paid_amount 
        data ["get_pending_amount"] =instance.get_pending_amount 
        data ['is_invoice_paid'] =instance.is_invoice_paid
    
        return data    

    def create(self, validated_data):
        instance =  super().create(validated_data)
        pay_method =validated_data.get('payment_method',None)
        paid=validated_data.get('paid_amount',None)
        data ={
            "payment_method" :pay_method,
            'amount_paid' :paid,
            'invoice' :instance
        }
        ContractorInvoicePaymentHistory.objects.create(**data)
        return instance
    

class ProjectSubContractListSerializer(ModelSerializer):
    get_contract_invoice = ContractorInvoiceSerializer(many=True,read_only=True)

    class Meta:
        model = ProjectSubContract
        fields = ('id','get_contract_invoice')
    
    def to_representation(self, instance):
        data =super().to_representation(instance)

        data ["contractor_name"]  = instance.display
        data ["project_name"] = instance.project.proj_name
        data ['total_wages'] = instance.total_wages
        data ['total_amount'] =instance.get_contract_amount
        data ['total_service_amount'] =instance.total_service_amount
        data ['get_paid_amount'] =instance.get_paid_amount
        data ['get_pending_amount'] =instance.get_pending_amount
        data ['pending_invoice_amount'] =instance.pending_invoice_amount
        data ['paid_status'] = False if instance.get_pending_amount >0 else  instance.paid_status
        data ['invoiced_status'] =  instance.paid_status
        data ['from_date'] =instance.start_date
        data ['to_date'] =instance.end_date
        data ['is_contract_invoiced'] =instance.is_contract_invoiced
        # data ['get_contract_invoice'] =instance.get_contract_invoice
    
        return data
    

class ProjectSubContractLabourAttendenceSerializer(ModelSerializer):
    class Meta:
        model = ProjectSubContractLabourAttendence
        fields = "__all__"

    def to_representation(self, instance):
        data =super().to_representation(instance)

        data ["contractor_name"]  = instance.contract.display_contractor if instance.contract else None
        data ["project_name"]  = instance.contract.display if instance.contract else None
        data ["atten_id"]  = instance.id

        return data
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)

    #     company = instance.company
    #     created_by = instance.created_by
    #     contract = instance.contract

    #     company_representation = None
    #     created_by_representation = None
    #     contract_representation = None

    #     if company:
    #         company_representation = {
    #             'id': company.id,
    #             'name': company.name  
    #         }

    #     if created_by:
    #         created_by_representation = {
    #             'id': created_by.id,
    #             'name': created_by.name 
    #         }

    #     if contract:
    #         contract_representation = {
    #             'id': contract.id,
    #             'name': contract.display  
    #         }

    #     representation['company'] = company_representation
    #     representation['created_by'] = created_by_representation
    #     # representation['contract'] = contract_representation

    #     # Adding contractor_name
    #     if contract:
    #         representation['contractor_name'] = contract.display  

    #     return representation
    


    

class UserSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(write_only=True, required=True, max_length=6)  # Assuming pin is a 6-character string

    class Meta:
        model = CustomUser
        # fields = ('id', 'name', 'phone_number', 'password',)  #pin
        fields ="__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        pin = validated_data.pop('pin', None)  # Remove 'pin' from validated data
       # user = CustomUser.objects.create_user(**validated_data, pin=pin)  # Pass 'pin' to create_user method
        user = CustomUser.objects.create(**validated_data, pin=pin) 
        return user
    
    
class OTPVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(max_length=6)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'


class ProfitandLoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


    def to_representation(self, instance):
        print(instance)
        data =  super().to_representation(instance)
        data ["profit_or_loss"] = instance.loss_or_profit if instance.loss_or_profit else None
        data ["material_expense"] = instance.purchace_expense if instance.purchace_expense else None
        data ["salary_expense"] = instance.labour_salary + instance.employee_salary
        data ["other_expense"] = instance.site_expense if instance.site_expense else None
        data ["subcontract_expense"] =  instance.subcontract_expense  if instance.subcontract_expense else None
        return  data
    
# ---------------------------------------------------------------------------------
class SalaryReceiptHistorySerializer(ModelSerializer):
     
    class Meta:
        model = SalaryPaymentHistory
        fields = '__all__'



    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["payment_method"] =instance.get_payment_method
        # data ["get_paid_amount"] =instance.get_paid_amount
        # data['get_pending_amount'] =instance.get_pending_amount
        # data ['get_total_amount'] =instance.get_total_amount
        # data['is_paid'] =instance.is_paid
        return data



class EmployeeSalaryReceiptHistorySerializer(ModelSerializer):
    
    class Meta:
        model = SalaryReceipt
        fields = ('id',"payment_date",'amount_paid','get_total_amount',"payment_amount",'transaction_id','payment_method','payment_period_start','payment_period_end','employee')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["payment_method"] =instance.get_payment_method
        data ["get_paid_amount"] =instance.get_paid_amount
        data['get_pending_amount'] =instance.get_pending_amount
        data ['get_total_amount'] =instance.get_total_amount
        data['is_paid'] =instance.is_paid
        return data
    
    def create(self, validated_data):
        # invoice = validated_data.get('invoice',None)
        # invoice.update_status()
        return super().create(validated_data)
    


class LabourSalaryReceiptHistorySerializer(ModelSerializer):
    get_payment_history = SalaryReceiptHistorySerializer(many=True,read_only=True)
    class Meta:
        model = SalaryReceipt
        fields = ('id',"payment_date",'amount_paid','get_total_amount',"payment_amount",'transaction_id',
                  'payment_method','payment_period_start','payment_period_end','labour','get_payment_history')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["payment_method"] =instance.get_payment_method
        data ["get_paid_amount"] =instance.get_paid_amount
        data['get_pending_amount'] =instance.get_pending_amount
        data ['get_total_amount'] = instance.get_total_amount
        data['is_paid'] =instance.is_paid
        return data
    
    def create(self, validated_data):
        instance =  super().create(validated_data)
        pay_method =validated_data.get('payment_method',None)
        paid=validated_data.get('amount_paid',None)
        data ={
            "payment_method" :pay_method,
            'amount_paid' :paid,
            'receipt' :instance
        }
        SalaryPaymentHistory.objects.create(**data)
        return instance
    

    
class EmployeeSalarySerializer(serializers.ModelSerializer):
    # get_salary_receipts = EmployeeSalaryReceiptHistorySerializer(many=True,read_only=True)
    class Meta:
        model = Employee
        fields =('id',"name")


    def to_representation(self, instance):
        request = self.context.get('request')
        date = None
        # print(request)
        if request:
            query_params = request.query_params
            query_date= request.GET.get('salary_date')
            if query_date:
                date = get_date_object(query_date)

        data =  super().to_representation(instance)
        data ["salary"],data ['paid'] ,data['pending']  ,data ["start_date"] ,data ["end_date"],data['is_paid'] = instance.this_month_salary(date) if instance.this_month_salary else (None,None,None,None,None,None)
        # data ['paid'] ,data['pending'] =  instance.get_paid_and_pending(date) if instance.get_paid_and_pending else (None,None,None)
   
        return  data





class CompanyLabourSalarySerializer(serializers.ModelSerializer):
    get_salary_receipts = LabourSalaryReceiptHistorySerializer(many=True,read_only=True)
    class Meta:
        model = CompanyLabours
        fields =('id',"name",'get_salary_receipts')


    def to_representation(self, instance):
        request = self.context.get('request')
        date = None
        # print(request)
        if request:
            query_params = request.query_params
            query_date= request.GET.get('date')
            if query_date:
                date = get_date_object(query_date)

        data =  super().to_representation(instance)
        data ["salary"],data ["start_date"] ,data ["end_date"],data ["days"],data['is_pending'] =  instance.total_salary_for_presented_days if instance.total_salary_for_presented_days else  (None,None,None,None,None,None)
        data ['get_pending_amount'] = instance.get_pending_amount
        return  data
    



    # -----------------------------------------------


class ProjectLabourAttendenceSerializer(serializers.ModelSerializer):
    # clock_in = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p', '%H:%M:%S'], required=False, allow_null=True)
    # clock_out = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p', '%H:%M:%S'], required=False, allow_null=True)
   
    class Meta:
        model = ProjectLabourAttendence
        fields = "__all__"


    # def create(self, validated_data):
        
    #     request =self.context["request"]
    #     user=request.user
    #     labour = validated_data["labour"] 
    #     obj=ProjectLabourAttendence.objects.filter(labour=labour,date=datetime.today()).last()
    #     if not obj:
    #        instance= self.perform_create(validated_data)
    #     else:
    #        instance= self.perform_update(obj,validated_data)
    #     return instance
   
    
    # def perform_create(self,validated_data):
    #     validated_data["clock_in"] =timezone.localtime(timezone.now()).time()
    #     return super().create(validated_data)
    

    # def perform_update(self, instance, validated_data):
    #     if instance.clock_out:
    #        raise serializers.ValidationError({"details":"You have already logged out"})
    #     instance.clock_out =timezone.localtime(timezone.now()).time()
    #     instance.save()
    #     return instance
    

    def to_representation(self, instance):
        data =super().to_representation(instance)

        data ["labour_name"]  = instance.labour.display if instance.labour else None
        data ["project_name"]  = instance.project.display if instance.project else None
        data ["atten_id"]  = instance.id

        return data
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)

    #     company = instance.company
    #     project = instance.project
    #     labour = instance.labour

    #     company_representation = None
    #     project_representation = None
    #     labour_representation = None

    #     if company:
    #         company_representation = {
    #             'id': company.id,
    #             'name': company.name  
    #         }
        
    #     if project:
    #         project_representation = {
    #             'id': project.id,
    #             'name': project.proj_name  
    #         }
        
    #     if labour:
    #         labour_representation = {
    #             'id': labour.id,
    #             'name': labour.name 
    #         }

    #     representation['company'] = company_representation
    #     representation['project'] = project_representation
    #     representation['labour'] = labour_representation

    #     return representation
    

""" empoyee Attendance setializrs """
class EmployeeAttendenceSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ["id"]


    def to_representation(self, instance):
        data =super().to_representation(instance)

        data ["employee_name"]  = instance.name if instance.name else None
        data ["employee"]  = instance.id
        data ["project"],data ["project_name"],data['clock_in'],data['clock_out'],data["over_time"],data['present'],data['atten_id']= instance.get_today_attendence 
        data['date'] =get_today()
        
        return data
    

class AttendenceSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"


    def to_representation(self, instance):
        data =super().to_representation(instance)

        data ["employee_name"]  = instance.employee.name if instance.employee else None
        data ["employee"]  = instance.employee.id if instance.employee else None
        data ["project_name"]  = instance.project.display if instance.project else None
        data ["atten_id"]  = instance.id
        data['date'] =get_today()
        
        return data



""" labour attendence serialisers  """
class LabourAttendenceSerialiser(serializers.ModelSerializer):

    class Meta:
        model = CompanyLabours
        fields = ["id",]


    def to_representation(self, instance):
        data =super().to_representation(instance)

        data ["labour_name"]  = instance.name if instance.name else None
        data ["labour"]  = instance.id
        data ["project"],data ["project_name"],data['clock_in'],data['clock_out'],data["over_time"],data['present'],data['atten_id']= instance.get_today_attendence 
        data['date'] =get_today()
        
        return data
                                                                                    

class DummyProjectSubContractLabourAttendenceSerializer(ModelSerializer):
    class Meta:
        model = ProjectSubContractLabourAttendence
        fields = "__all__"

class ProjectSubContractAttendenceSerialiser(serializers.ModelSerializer):
    get_today_attendence = DummyProjectSubContractLabourAttendenceSerializer()
    class Meta:
        model = ProjectSubContract
        fields = ["id",'get_today_attendence']


    def to_representation(self, instance):
        data =super().to_representation(instance)
        data['contractor_name'] = instance.display_contractor
        data['project_name'] = instance.display
        data ["atten_id"]  = instance.get_today_attendence.id if instance.get_today_attendence else 0
        data['date'] = get_today()

        if instance.get_today_attendence:
            nested_data = data.pop("get_today_attendence", {})
            combined_data = {**data, **nested_data}
        else:
            combined_data = data

        return combined_data

    







class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'
    
    def to_representation(self, instance):
     representation = super().to_representation(instance)
    
     project_name = instance.project_name 
     project_name_representation = None

     if project_name:
        project_name_representation = {
            'id': project_name.id,
            'name': project_name.proj_name,
        },     

     return {
        'id': representation['id'],
        'file': representation['file'],             
        'project_name': project_name_representation,     
     }
    
class EmployeeProfileSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    class Meta:
        model = EmployeeProfile
        fields = ['employee', 'email', 'mobile', 'address','image']

class DailyMaterialUsageSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyMaterialUsage
        fields = '__all__'
    
    def to_representation(self, instance):
     representation = super().to_representation(instance)
    
     stock = instance.stock
     user = instance.user 
     material= instance.material

     stock_representation = None
     user_representation = None
     material_representation = None

     if stock:
        stock_representation = {
            'id': stock.id,
            'name': stock.name,
        },     
     
     if user:
        user_representation = {
            'id': user.id,
            'name': user.name,
        },
     
     if material:
        material_representation = {
            'id': material.id,
            'name': material.item,
        },

     return {
        'id': representation['id'],
        'date': representation['date'],  
        'used': representation['used'], 
        'stock': stock_representation,  
        'user': user_representation, 
        'material': material_representation,     
     }
    
class ProjectMachineExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMachineExpense
        fields = '__all__'
    
    def to_representation(self, instance):
     data = super().to_representation(instance)
    
     project = instance.project
     machine = instance.machine 
     payment_schedule= instance.payment_schedule

     project_representation = None
     machine_representation = None
     payment_schedule_representation = None

     if machine:
       data ["machine"] = {
            'id': machine.id,
            'name': machine.name,
        },
     
     if payment_schedule:
        data ["payment_schedule"] = {
            'id': payment_schedule.id,
            'name': payment_schedule.days,
        },

     return data
    
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        #fields = ['id', 'name', 'monthly_working_days', 'monthly_paid_leaves']
        fields = '__all__'

class CompanyProfileSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = CompanyProfile
        #fields = ['id', 'company', 'email', 'contact_number', 'gst_number', 'address', 'area']
        fields = '__all__'    

class PaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSchedule
        fields = '__all__'

class PettyCashSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField()

    class Meta:
        model = PettyCash
        fields = ['id', 'amount', 'attachment', 'company', 'date', 'employee', 'particular', 'site_location','payment_method'] 

class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['id', 'project', 'date', 'receipt_number', 'payment_mode', 'payment_amount']




class dailyTaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dailytask
        fields = '__all__'
# class SiteAllocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SiteAllocation
#         fields = '__all__'

#     def to_representation(self, instance):
#         data =super().to_representation(instance)
#         data ["date"]=instance.get_date
#         data["project_name"] = instance.project.proj_name if instance.project else None
#         data["employee_name"] = instance.employee.name if instance.employee else None
#         data["labour_name"] = "dfsdfsfs"
#         data["created_by_name"] = instance.created_by.name if instance.created_by else None
        
#         return data



class SiteAllocationEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteAllocation
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["date"] = instance.get_date
        data["project_name"] = instance.project.proj_name if instance.project else None
        data["employee_name"] = instance.employee.name if instance.employee else None
        data["created_by_name"] = instance.created_by.name if instance.created_by else None
        return data
    
class SiteAllocationLabourSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteAllocation
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["date"] = instance.get_date
        data["project_name"] = instance.project.proj_name if instance.project else None
        data["labour_name"] = instance.labour.name if instance.labour else None
        data["created_by_name"] = instance.created_by.name if instance.created_by else None
        return data
    
