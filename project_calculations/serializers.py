from rest_framework import serializers
from .. import models


class ProfitAndLossProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ProfitAndLossProject
		fields = '__all__'

class CFProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.CFProject
		fields = '__all__'

class ProjectBalanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ProjectBalance
		fields = '__all__'

class ProjectFinancialIndicatorSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ProjectFinancialIndicator
		fields = '__all__'