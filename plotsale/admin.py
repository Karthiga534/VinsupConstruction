from .models import *
from django.contrib import admin

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(PlotType)
class PlotTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SoilType)
class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(BrokerPost)
class BrokerPostAdmin(admin.ModelAdmin):
    list_display = ('plotarea',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin): 
    list_display = ('name',)

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin): 
    list_display = ('name',)

@admin.register(SitePosting)
class SitePostingAdmin(admin.ModelAdmin):
    list_display = ('plot_id',)

@admin.register(Queries)
class QueriesAdmin(admin.ModelAdmin):
    list_display = ('plot_id',)

@admin.register(PlotSales)
class PlotSalesAdmin(admin.ModelAdmin):
    list_display = ('plot_id',)

