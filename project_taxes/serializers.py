from rest_framework import serializers
from . import models
from projects.models import Project
from projects.serializers import DinamycFieldsModelSerializer


class TaxPrmSerializer(DinamycFieldsModelSerializer):
	active = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = models.TaxPrm
		fields = '__all__'

	def get_active(self, obj):
		return True
				
class DiscountRateSerializer(DinamycFieldsModelSerializer):
	active = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = models.DiscountRate
		fields = '__all__'

	def get_active(self, obj):
		return True