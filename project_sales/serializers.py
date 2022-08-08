from rest_framework import serializers
from . import models
from projects.serializers import DinamycFieldsModelSerializer

class SalesInitSerializer(DinamycFieldsModelSerializer):
	active = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = models.SalesInit
		fields = '__all__'

	def get_active(self, obj):
		if obj.start_date and obj.end_date:
			return True
		else:
			return False

class OpexVariantSerializer(DinamycFieldsModelSerializer):
	expenses = serializers.DictField(source='get_total_opexs', read_only=True)
	active = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = models.OpexVariant
		fields = '__all__'

	def get_active(self, obj):
		return True
				
class OpexSerializer(serializers.ModelSerializer):
	total_pays = serializers.DictField(source='get_total_pays', read_only=True)
	class Meta:
		model = models.Opex
		fields = '__all__'