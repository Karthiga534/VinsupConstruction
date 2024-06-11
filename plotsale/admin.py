from .models import *
from django.contrib import admin

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(PlotType)
class PlotTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SoilType)
class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
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

