from django.db import models
from django.utils import timezone

class Area(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return self.name
    
class PropertyType(models.Model):
    name = models.CharField(max_length=50) 
    code = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return self.name
    
class PlotType(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return self.name
    
class SoilType(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return self.name
    
class Post(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return self.name
    
class Status(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return self.name
    
class Water(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return self.name
    
class PaymentStatus(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return self.name
    
    
class Agent(models.Model):
    date=models.DateField(auto_now_add=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    img =models.FileField(upload_to="doc",null=True,blank=True)
    phone=models.CharField(max_length=10, unique=True,null=True,blank=True)
    email=models.EmailField(max_length=100,unique=True,null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    aadhaar = models.CharField(max_length=50, null=True, blank=True)
    pan = models.CharField(max_length=50, null=True, blank=True)
    voter = models.CharField(max_length=50, null=True, blank=True)
    bankname = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    accountno = models.CharField(max_length=50, null=True, blank=True)
    ifsc = models.CharField(max_length=50, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE,null=True,blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
        
class BrokerPost(models.Model):
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE,null=True,blank=True)
    img = models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True,blank=True)
    plotarea = models.CharField(max_length=500)
    area = models.ForeignKey(Area, on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    map = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    soil_type = models.ForeignKey(SoilType, blank=True , null =True, on_delete=models.CASCADE)
    plot_type = models.ForeignKey(PlotType, blank=True , null =True, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    water_type = models.ForeignKey(Water, on_delete=models.CASCADE,null=True,blank=True)
    start_date = models.DateTimeField(null=True, blank=True) 
    end_date = models.DateTimeField(null=True, blank=True)   
    publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            now = timezone.now()
            self.publish = self.start_date <= now <= self.end_date
        super().save(*args, **kwargs)

    def __str__(self):
        return self.plotarea

class BrokerPayment(models.Model):
    broker_post = models.ForeignKey(BrokerPost, on_delete=models.CASCADE, related_name='payments')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True) 
    payment_id = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    payment_method = models.ForeignKey(PaymentMethod, blank=True , null =True, on_delete=models.CASCADE)
    payment_status = models.ForeignKey(PaymentStatus, blank=True , null =True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Payment {self.payment_id} for BrokerPost {self.broker_post.plotarea}"

class SitePosting(models.Model):
    date=models.DateField(auto_now_add=True, null=True, blank=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE,null=True,blank=True)
    plot_id = models.CharField(max_length=20, blank=True , null =True)
    plot_type = models.ForeignKey(PlotType, blank=True , null =True, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, blank=True , null =True)
    address = models.CharField(max_length=255,null=True,blank=True)
    soil_type = models.ForeignKey(SoilType, blank=True , null =True, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True,blank=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.plot_id
    
class Queries(models.Model):
    date=models.DateField(auto_now_add=True, null=True, blank=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE,null=True,blank=True)
    plot_id = models.CharField(max_length=20)
    plot_type = models.ForeignKey(PlotType, blank=True , null =True, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=255,null=True,blank=True)
    soil_type = models.ForeignKey(SoilType, blank=True , null =True, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True,blank=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.plot_id
    
class PlotSales(models.Model):
    date=models.DateField(auto_now_add=True, null=True, blank=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE,null=True,blank=True)
    plot_id = models.CharField(max_length=20)
    plot_type = models.ForeignKey(PlotType, blank=True , null =True, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=255,null=True,blank=True)
    soil_type = models.ForeignKey(SoilType, blank=True , null =True, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True,blank=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.plot_id
    

