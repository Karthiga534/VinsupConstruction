from django.db import models

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


    def __str__(self):
        return self.plotarea

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
    

