from rest_framework import serializers
from . import models
from projects.models import Project

class TaxPrmSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.TaxPrm
		fields = '__all__'

class DiscountRateSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.DiscountRate
		fields = '__all__'
