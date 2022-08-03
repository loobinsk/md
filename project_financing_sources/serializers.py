from rest_framework import serializers
from . import models

class OwnFundVariantSerializer(serializers.ModelSerializer):
	total_own_funds = serializers.IntegerField(source='get_total_own_funds', read_only=True)
	class Meta:
		model = models.OwnFundVariant
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

class OwnFundSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.OwnFund
		fields = '__all__'

class CreditVariantSerializer(serializers.ModelSerializer):
	total_contributions = serializers.IntegerField(read_only=True)
	class Meta:
		model = models.CreditVariant
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

class CreditSerializer(serializers.ModelSerializer):
	credit_share = serializers.FloatField(read_only=True)
	class Meta:
		model = models.Credit
		fields = '__all__'

class LeasingContractVariantSerializer(serializers.ModelSerializer):
	total_pays = serializers.IntegerField(read_only=True)
	class Meta:
		model = models.LeasingContractVariant
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

class LeasingContractSerializer(serializers.ModelSerializer):
	price_object = serializers.FloatField(read_only=True)
	accounting_date = serializers.DateTimeField(read_only=True)
	total_pays = serializers.DictField(read_only=True)
	class Meta:
		model = models.LeasingContract
		fields = '__all__'

class WorkingCapitalParameterSerializer(serializers.ModelSerializer):
	share_of_sales = serializers.FloatField(read_only=True)
	share_of_purchases = serializers.FloatField(read_only=True)
	class Meta:
		model = models.WorkingCapitalParameter
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)