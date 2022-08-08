from rest_framework import serializers
from . import models
from projects.serializers import DinamycFieldsModelSerializer


class OwnFundVariantSerializer(DinamycFieldsModelSerializer):
	total_own_funds = serializers.IntegerField(source='get_total_own_funds', read_only=True)
	active = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = models.OwnFundVariant
		fields = '__all__'

	def get_active(self, obj):
		return True

class OwnFundSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.OwnFund
		fields = '__all__'

class CreditVariantSerializer(DinamycFieldsModelSerializer):
	total_contributions = serializers.IntegerField(read_only=True)
	active = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = models.CreditVariant
		fields = '__all__'

	def get_active(self, obj):
		return True

class CreditSerializer(serializers.ModelSerializer):
	credit_share = serializers.FloatField(read_only=True)
	class Meta:
		model = models.Credit
		fields = '__all__'

class LeasingContractVariantSerializer(DinamycFieldsModelSerializer):
	total_pays = serializers.IntegerField(read_only=True)
	active = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = models.LeasingContractVariant
		fields = '__all__'

	def get_active(self, obj):
		return True

class LeasingContractSerializer(serializers.ModelSerializer):
	price_object = serializers.FloatField(read_only=True)
	accounting_date = serializers.DateTimeField(read_only=True)
	total_pays = serializers.DictField(read_only=True)
	class Meta:
		model = models.LeasingContract
		fields = '__all__'

class WorkingCapitalParameterSerializer(DinamycFieldsModelSerializer):
	share_of_sales = serializers.FloatField(read_only=True)
	share_of_purchases = serializers.FloatField(read_only=True)
	active = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = models.WorkingCapitalParameter
		fields = '__all__'

	def get_active(self, obj):
		return True
