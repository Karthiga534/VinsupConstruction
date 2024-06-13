from . import views
from django.urls import path

urlpatterns = [

    path('property_types/',views.get_property_types,name='property_types'), # GET
    path('plot_types/',views.get_plot_types,name='plot_type'), # GET
    path('soil_types/',views.get_soil_types,name='soil_types'), # GET
    path('status_types/',views.get_status_types,name='status_types'), # GET

    path('sitepostings/', views.site_postings, name='site_postings_list'), # GET & POST
    path('sitepostings/<int:pk>/', views.site_postings, name='site_postings_detail'), # GET --> PK
    path('siteposting/<int:pk>/', views.site_posting_detail, name='site_posting_detail'), # GET --> PK ( PUT, DELETE )

    path('queries/', views.queries, name='queries'), # GET & POST
    path('queries/<int:pk>/', views.queries, name='queries_detail'), # GET --> PK
    path('queriess/<int:pk>/', views.queries_detail, name='queries_detail'), # GET --> PK ( PUT, DELETE )

    path('plotsales/', views.plotsales, name='plotsales'), # GET & POST
    path('plotsales/<int:pk>/', views.plotsales, name='plotsales_detail'), # GET --> PK
    path('plotsaless/<int:pk>/', views.plotsales_detail, name='plotsales_detail'), # GET --> PK ( PUT, DELETE )


     path('area/',views.area,name='area'),
     path('property_type/',views.property_type,name='property_type'),

]
