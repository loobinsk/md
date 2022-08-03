from rest_framework import serializers
from . import models
from projects.models import Project

class TaxPrmSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.TaxPrm
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)
				
class DiscountRateSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.DiscountRate
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)