
from app.auth_models import *
# from .models import Purchase
from rest_framework import serializers
from rest_framework.serializers import *
from django.contrib.auth.hashers import make_password
from .utils import *
from django.db import transaction,IntegrityError





class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class AssetTypeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields =("id",'name','code')


class AssetListSerialiser(serializers.ModelSerializer):
    gettype= AssetTypeSerialiser(read_only=True,many=False)
    class Meta:
        model = CompanyAsset
        fields = '__all__'

    
    def validate(self, data):
        asset_type = data.get('type', None)
        if asset_type is not None:
            file = data.get('file')
            if file:
                validate_file_type(file, asset_type.code)
        return data




class CompanygetSerializer(serializers.ModelSerializer):
    assetlist=AssetListSerialiser(many=True)
    class Meta:
        model = Company
        fields = '__all__'

#------------------------------------------------------------------------------------------------------------------------------------------------------------


class OwnerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerInfo
        fields = '__all__'


class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


    # def validate_phone(self, value):
    #     # Your validation logic goes here
    #     # For example, checking if a branch with this phone already exists
    #     if Company.objects.filter(phone=value).exists():
    #         raise serializers.ValidationError("Branch with this phone already exists.")
    #     return value

    
    # def to_internal_value(self, data):
    #     return data
    

class OwnerInfoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerInfo
        fields = '__all__'
        


# class AdminOwnerSerializer(serializers.ModelSerializer):
    # company = CompanygetSerializer(many=False,required=False)
    # getcompanies =CompanygetSerializer(many=True,required=False)
    # employee=EmployeeSerializer(many=False,required=False)
    # owner =OwnerInfoSerializer(many=False,required=False)
    # address =serializers.CharField(required=False)
    # proof =serializers.FileField(required=False)

    # company_email = serializers.EmailField(required=True)
    # company_name = serializers.CharField(max_length=255 ,required=True)
    # company_phone_number = serializers.CharField(max_length=10 ,required=True)
    # company_address = serializers.CharField(max_length=255,required=True)


class AdminOwnerSerializer(serializers.ModelSerializer):
    company = CompanyCreateSerializer()
    owner = OwnerInfoCreateSerializer()

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone_number', 'company', 'owner',  'proof', 'image', 'admin')


    
    def create(self, validated_data):
        company_data = validated_data.pop('company')
        owner_data = validated_data.pop('owner')

        validated_data["pin"]= pin = get_pin()
        password =get_password(validated_data["name"])
        validated_data["password"]=  make_password(password)
        print(password)
        # custom_user = CustomUser.objects.create( **validated_data)
        try:
            with transaction.atomic():
                # custom_user = CustomUser.objects.create_user(**validated_data)
                custom_user =custom_user_create(validated_data)
                custom_user.set_password(password)
                custom_user.is_owner = True
                custom_user.admin = True
                custom_user.save()

                company_data["admin"] = owner_data["owner"] = custom_user
                company = Company.objects.create(**company_data)
                owner = OwnerInfo.objects.create(**owner_data)
                
                msg = f"Welcome {custom_user.name}. Your Employee account created successfully. This is your password {password} and Mpin {pin} vinsupinfotech."
                send_sms(custom_user.phone_number, msg, templateid=False)
                
        except IntegrityError as e:
            raise serializers.ValidationError({"detail": str(e)})

        return custom_user
        # custom_user =custom_user_create(validated_data)
        # custom_user.is_owner=True
        # custom_user.admin=True
        # custom_user.save()
        # company_data["admin"] =owner_data["owner"]=custom_user
        # company = Company.objects.create(**company_data)
        # owner = OwnerInfo.objects.create(**owner_data)
        # msg=f"Welcome {custom_user.name} Your Employee account created successfully. This is your password {password} and Mpin {pin} vinsupinfotech."
        # send_sms(custom_user.phone_number,msg,templateid=False)
        # return custom_user



def custom_user_create(validated_data):
    try:
            user = CustomUser.objects.create(**validated_data)
            return user
    except IntegrityError as e:
        if 'UNIQUE constraint failed: app_customuser.email' in str(e):
            raise serializers.ValidationError({'email': ['A user with that email already exists.']})
        else:
            raise serializers.ValidationError({'detail': ['An error occurred. Please try again.']})


class CompanyupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    def to_internal_value(self, data):
        return data
    





# for updating admin informAation without owner
class AdminOwnerUpdateSerializer(serializers.ModelSerializer):
    company = CompanyupdateSerializer()
    owner = OwnerInfoCreateSerializer()

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone_number', 'company', 'owner',  'proof', 'image', 'admin')


    def update(self, instance, validated_data):
        print("enter" ,validated_data)
        company_data = validated_data.pop('company', None)
        owner_data = validated_data.pop('owner', None)

        # Update CustomUser fields
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.proof = validated_data.get('proof', instance.proof)
        instance.image = validated_data.get('image', instance.image)
        instance.admin = validated_data.get('admin', instance.admin)
        instance.save()

        # # Update Company instance if data is provided
        # if company_data and instance.company :
        #     company_phone = company_data.get('phone')
        #     if company_phone != instance.company.phone and Company.objects.filter(phone=company_phone).exists():
        #         raise serializers.ValidationError({'company' :{'phone': ['Phone Number already exists with another Company']}})
        #     company_serializer = CompanyCreateSerializer(instance.company, data=company_data)
        #     if company_serializer.is_valid():
        #         company_serializer.save()

        # # Update OwnerInfo instance if data is provided
        # if owner_data:
        #     owner_serializer = OwnerInfoCreateSerializer(instance.owner, data=owner_data)
        #     if owner_serializer.is_valid():
        #         owner_serializer.save()

        # return instance
    

        try:
            with transaction.atomic():
               # Update Company instance if data is provided
                if company_data and instance.company :
                    company_phone = company_data.get('phone')
                    if company_phone != instance.company.phone and Company.objects.filter(phone=company_phone).exists():
                        raise serializers.ValidationError({'company' :{'phone': ['Phone Number already exists with another Company']}})
                    company_serializer = CompanyCreateSerializer(instance.company, data=company_data)
                    if company_serializer.is_valid():
                        company_serializer.save()

                # Update OwnerInfo instance if data is provided
                if owner_data:
                    owner_serializer = OwnerInfoCreateSerializer(instance.owner, data=owner_data)
                    if owner_serializer.is_valid():
                        owner_serializer.save()
                
        except IntegrityError as e:
            raise serializers.ValidationError({"detail": str(e)})

        return instance



# for upgrading admin to owner
class UpgradeUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone_number')


    def update(self, instance, validated_data):

        # FOR OWNER
        with transaction.atomic():
            pin = get_pin()
            password =get_password(validated_data["name"])
            validated_data["password"]=  make_password(password)
            validated_data["pin"]= pin
            validated_data["is_owner"] =True
            # owner=CustomUser.objects.create( **validated_data)

            try:
                with transaction.atomic():
                    owner =custom_user_create(validated_data)
                    msg=f"Welcome {owner.name} Your Employee account created successfully. This is your password {password} and Mpin {pin} vinsupinfotech."
                    send_sms(owner.phone_number,msg,templateid=False)
                    # owner.owner =True   
                    owner_info=instance.owner
                    owner_info.set_owner(owner)
                    # owner_info.owner =owner
                    # owner_info.save()

                    company=instance.company
                    company.owner =owner
                    company.save()

                    # FOR change user to ADMIN and remove owner
                    instance.is_owner=False
                    instance.save()
                
            except IntegrityError as e:
                raise serializers.ValidationError({"detail": str(e)})

            return instance
            owner =custom_user_create(validated_data)
            msg=f"Welcome {owner.name} Your Employee account created successfully. This is your password {password} and Mpin {pin} vinsupinfotech."
            send_sms(owner.phone_number,msg,templateid=False)
            # owner.owner =True   
            owner_info=instance.owner
            owner_info.set_owner(owner)
            # owner_info.owner =owner
            # owner_info.save()

            company=instance.company
            company.owner =owner
            company.save()

            # FOR change user to ADMIN and remove owner
            instance.is_owner=False
            instance.save()
    
        return instance
    



# branch create serialiser

class BranchCreateSerializer(serializers.ModelSerializer):
    company = CompanyCreateSerializer()
   

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone_number', 'company', 'image', 'admin',"is_owner")


    
    def create(self, validated_data):
        company_data = validated_data.pop('company')
        pin = get_pin()
        password =get_password(validated_data["name"])
        validated_data["pin"]= pin
        validated_data["password"]=  make_password(password)
        # custom_user = CustomUser.objects.create( **validated_data)

        try:
            with transaction.atomic():
                    custom_user =custom_user_create(validated_data)
                    custom_user.admin=True
                    custom_user.save()
                    company_data["admin"] =custom_user
                    company = Company.objects.create(**company_data)
            
                    msg=f"Welcome {custom_user.name} Your Employee account created successfully. This is your password {password} and Mpin {pin} vinsupinfotech."
                    send_sms(custom_user.phone_number,msg,templateid=False)
                
        except IntegrityError as e:
                raise serializers.ValidationError({"detail": str(e)})

        return custom_user
        custom_user =custom_user_create(validated_data)
        custom_user.admin=True
        custom_user.save()
        company_data["admin"] =custom_user
        company = Company.objects.create(**company_data)
  
        msg=f"Welcome {custom_user.name} Your Employee account created successfully. This is your password {password} and Mpin {pin} vinsupinfotech."
        send_sms(custom_user.phone_number,msg,templateid=False)
        return custom_user
    

    def update(self, instance, validated_data):
        company_data = validated_data.pop('company')
        pin = get_pin()
        password =get_password(validated_data["name"])
        validated_data["pin"]= pin
        validated_data["password"]=  make_password(password)
        # custom_user = CustomUser.objects.create( **validated_data)

        try:
            with transaction.atomic():
                    custom_user = custom_user_create(validated_data)
                    custom_user.admin=True
                    custom_user.save()
                    company_data["admin"] =custom_user
                    company_data["owner"] =instance
                    company = Company.objects.create(**company_data)
            
                    msg=f"Welcome {custom_user.name} Your Employee account created successfully. This is your password {password} and Mpin {pin} vinsupinfotech."
                    send_sms(custom_user.phone_number,msg,templateid=False)
                
        except IntegrityError as e:
                raise serializers.ValidationError({"detail": str(e)})

        return custom_user
        custom_user =custom_user_create(validated_data)
        custom_user.admin=True
        custom_user.save()
        company_data["admin"] =custom_user
        company_data["owner"] =instance
        company = Company.objects.create(**company_data)
  
        msg=f"Welcome {custom_user.name} Your Employee account created successfully. This is your password {password} and Mpin {pin} vinsupinfotech."
        send_sms(custom_user.phone_number,msg,templateid=False)
        return custom_user

        return super().update(instance, validated_data)
       
    
# -----------------------------------------------------------------------------------------------------------------

# company profile for admin user

class OwnergetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OwnerInfo
        fields = '__all__'



class CompanygetSerializer(serializers.ModelSerializer):
    assetlist=AssetListSerialiser(many=True)
    class Meta:
        model = Company
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data ["plan_name"] = instance.plan.name if instance.plan else None
        return data

class CompanyAdminProfileSerializer(serializers.ModelSerializer):
    company = CompanygetSerializer()
    owner = OwnergetSerializer()

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone_number', 'company', 'owner',  'proof', 'image', 'admin')
