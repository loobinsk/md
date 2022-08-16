from rest_framework import serializers
from . import models


class ProfitAndLossProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ProfitAndLossPlan
		fields = '__all__'

class CFProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.CashFlowPlan
		fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Balance
		fields = '__all__'

class FinancialIndicatorSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ResultFinancialAnalys
		fields = '__all__'

class MainParameterSerializer(serializers.ModelSerializer):
	duration=serializers.CharField(read_only=True)
	class Meta:
		model = models.MainParameter
		exclude = ['id', 'calculation',]

class FundingAmountSerializer(serializers.ModelSerializer):
	total_amount = serializers.FloatField(read_only=True)
	class Meta:
		model = models.FundingAmount
		exclude = ['id', 'calculation',]

class AnnualAverageSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AnnualAverage
		exclude = ['id', 'calculation',]

class BasicIndicatorSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.BasicIndicator
		exclude = ['id', 'calculation',]

class PaybackProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.PaybackProject
		exclude = ['id', 'calculation',]

class CalculationSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Calculation
		exclude = ['id']

class RatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Rating
		exclude = ['id', 'calculation',]

class CalculationResultSerializer(serializers.ModelSerializer):
	rating = RatingSerializer(read_only=True)
	payback_project = PaybackProjectSerializer(read_only=True)
	basic_indicators = BasicIndicatorSerializer(read_only=True)
	annual_average = AnnualAverageSerializer(read_only=True)
	funding_amounts = FundingAmountSerializer(read_only=True)
	main_parameters = MainParameterSerializer(read_only=True)
	class Meta:
		model = models.Calculation
		fields = [
				'rating',
				'project',
				'payback_project', 
				'basic_indicators', 
				'annual_average', 
				'funding_amounts', 
				'main_parameters']

class ProfitAndLossSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ProfitAndLossPlan
		exclude = ['id']

class CashFlowPlanSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.CashFlowPlan
		exclude = ['id']

class BalanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Balance
		exclude = ['id']

class ResultFinancialAnalysSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.ResultFinancialAnalys
		exclude = ['id']