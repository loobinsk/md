from rest_framework import serializers
from . import models


class SalesInitSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.SalesInit
		fields = '__all__'

class OpexVariantSerializer(serializers.ModelSerializer):
	expenses = serializers.DictField(source='get_total_opexs', read_only=True)
	class Meta:
		model = models.OpexVariant
		fields = '__all__'

class OpexSerializer(serializers.ModelSerializer):
	total_pays = serializers.DictField(source='get_total_pays', read_only=True)
	class Meta:
		model = models.Opex
		fields = '__all__'