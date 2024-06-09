from .models import *
from rest_framework import serializers

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

