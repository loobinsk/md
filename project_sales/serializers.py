from rest_framework import serializers
from . import models


class SalesInitSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.SalesInit
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

class OpexVariantSerializer(serializers.ModelSerializer):
	expenses = serializers.DictField(source='get_total_opexs', read_only=True)
	class Meta:
		model = models.OpexVariant
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)
				
class OpexSerializer(serializers.ModelSerializer):
	total_pays = serializers.DictField(source='get_total_pays', read_only=True)
	class Meta:
		model = models.Opex
		fields = '__all__'