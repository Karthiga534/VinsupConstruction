from .models import *
from rest_framework import serializers

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'

class PlotTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotType
        fields = '__all__'

class SoilTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilType
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class SitePostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitePosting
        fields = '__all__'

class QueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queries
        fields = '__all__'

class PlotSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotSales
        fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'

                 















                 