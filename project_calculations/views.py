import traceback

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
#drf
from rest_framework import generics, filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
#import from this app
from .calc_funcs import profit_and_loss, flow_funds
from .calc_funcs import balance, results, total_fields
from .models import Calculation, ResultFinancialAnalys, Balance
from .models import ProfitAndLossPlan, CashFlowPlan, MainParameter
from .models import Rating, FundingAmount, AnnualAverage
from .models import BasicIndicator, PaybackProject
from . import serializers, permissions

from projects import choices
from projects.models import Project
#models
from project_sales.models import SalesInit, OpexVariant
from project_taxes.models import TaxPrm, DiscountRate
from project_economic_indicators.models import Capex
from project_financing_sources.models import OwnFundVariant, CreditVariant
from project_financing_sources.models import LeasingContractVariant, WorkingCapitalParameter
#serializers 
from project_sales.serializers import SalesInitSerializer, OpexVariantSerializer
from project_taxes.serializers import TaxPrmSerializer, DiscountRateSerializer
from project_economic_indicators.serializers import CapexSerializer
from project_financing_sources.serializers import OwnFundVariantSerializer, CreditVariantSerializer
from project_financing_sources.serializers import LeasingContractVariantSerializer, WorkingCapitalParameterSerializer




class TestView(APIView):

	def get(self, request):
		calc = Calculation.objects.first()
		ResultFinancialAnalys.objects.filter(calculation=calc).delete()
		Balance.objects.filter(calculation=calc).delete()
		CashFlowPlan.objects.filter(calculation=calc).delete()
		ProfitAndLossPlan.objects.filter(calculation=calc).delete()
		MainParameter.objects.filter(calculation=calc).delete()
		Rating.objects.filter(calculation=calc).delete()
		FundingAmount.objects.filter(calculation=calc).delete()
		AnnualAverage.objects.filter(calculation=calc).delete()
		BasicIndicator.objects.filter(calculation=calc).delete()
		PaybackProject.objects.filter(calculation=calc).delete()

		if not ProfitAndLossPlan.objects.filter(calculation=calc).exists():
			PL_LOAD_DATA = profit_and_loss.DBLoadData(calc)
			PL_LOAD_DATA.add_data_in_db()
		if not CashFlowPlan.objects.filter(calculation=calc).exists():
			FLDBLoadData = flow_funds.FLDBLoadData(calc)
			FLDBLoadData.add_data_in_db()
		if not Balance.objects.filter(calculation=calc).exists():
			BalanceDBLoadData = balance.BalanceDBLoadData(calc)
			BalanceDBLoadData.add_data_in_db()
		if not ResultFinancialAnalys.objects.filter(calculation=calc).exists():
			ResultsDBLoadData = results.ResultsDBLoadData(calc)
			ResultsDBLoadData.add_data_in_db()
		if not MainParameter.objects.filter(calculation=calc).exists():
			DBLoadData = total_fields.DBLoadData(calc)
			DBLoadData.load_data_in_db()
		return Response('все окей')

class CalculationEnums(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, pk):
		project = get_object_or_404(Project, pk=pk)
		sales = SalesInit.objects.filter(project=project)
		sales = SalesInitSerializer(sales, many=True, fields=('id', 'variant_name', 'active'), rename=True)
		opexs = OpexVariant.objects.filter(project=project)
		opexs = OpexVariantSerializer(opexs, many=True, fields=('id', 'variant_name', 'active'), rename=True)
		capexs = Capex.objects.filter(project=project)
		capexs = CapexSerializer(capexs, many=True, fields=('id', 'variant_name', 'active'),rename=True)
		taxs = TaxPrm.objects.filter(project=project)
		taxs = TaxPrmSerializer(taxs, many=True, fields=('id', 'variant_name', 'active'), rename=True)
		discount_rates = DiscountRate.objects.filter(project=project)
		discount_rates = DiscountRateSerializer(discount_rates, many=True, fields=('id', 'variant_name', 'active'), rename=True)
		own_funds = OwnFundVariant.objects.filter(project=project)
		own_funds = OwnFundVariantSerializer(own_funds, many=True, fields=('id', 'variant_name', 'active'), rename=True)
		credits = CreditVariant.objects.filter(project=project)
		credits = CreditVariantSerializer(credits, many=True,fields=('id', 'variant_name', 'active'), rename=True)
		leasings = LeasingContractVariant.objects.filter(project=project)
		leasings = LeasingContractVariantSerializer(leasings, many=True, fields=('id', 'variant_name', 'active'), rename=True)
		wk = WorkingCapitalParameter.objects.filter(project=project)
		wk = WorkingCapitalParameterSerializer(wk, many=True, fields=('id', 'variant_name', 'active'), rename=True)
		data = {
			'sales': sales.data,
			'opexs': opexs.data,
			'capexs': capexs.data,
			'taxs': taxs.data,
			'discount_rates': discount_rates.data,
			'own_funds': own_funds.data,
			'credits': credits.data,
			'leasings': leasings.data,
			'wk': wk.data,
		}
		return Response(data, status=status.HTTP_200_OK)

class CalculationView(generics.RetrieveUpdateAPIView):
	serializer_class = serializers.CalculationSerializer
	queryset = Calculation.objects.all()
	permission_classes = [permissions.IsOwner, IsAuthenticated]

class CalcResultsView(APIView):
	serializer = serializers.CalculationResultSerializer
	queryset = Calculation.objects.all()
	permission_classes = [IsAuthenticated]

	def get(self, request, pk):
		project = Project.objects.get(pk=pk, author=self.request.user)
		obj = self.queryset.get(project=project)
		serializer = self.serializer(obj)
		return Response(serializer.data)

	def post(self, request, pk, *args, **kwargs):
		project = Project.objects.get(pk=pk)
		calc = get_object_or_404(Calculation, project=project)

		ResultFinancialAnalys.objects.filter(calculation=calc).delete()
		Balance.objects.filter(calculation=calc).delete()
		CashFlowPlan.objects.filter(calculation=calc).delete()
		ProfitAndLossPlan.objects.filter(calculation=calc).delete()
		MainParameter.objects.filter(calculation=calc).delete()
		Rating.objects.filter(calculation=calc).delete()
		FundingAmount.objects.filter(calculation=calc).delete()
		AnnualAverage.objects.filter(calculation=calc).delete()
		BasicIndicator.objects.filter(calculation=calc).delete()
		PaybackProject.objects.filter(calculation=calc).delete()

		try:
			if not ProfitAndLossPlan.objects.filter(calculation=calc).exists():
				PL_LOAD_DATA = profit_and_loss.DBLoadData(calc)
				PL_LOAD_DATA.add_data_in_db()
			if not CashFlowPlan.objects.filter(calculation=calc).exists():
				FLDBLoadData = flow_funds.FLDBLoadData(calc)
				FLDBLoadData.add_data_in_db()
			if not Balance.objects.filter(calculation=calc).exists():
				BalanceDBLoadData = balance.BalanceDBLoadData(calc)
				BalanceDBLoadData.add_data_in_db()
			if not ResultFinancialAnalys.objects.filter(calculation=calc).exists():
				ResultsDBLoadData = results.ResultsDBLoadData(calc)
				ResultsDBLoadData.add_data_in_db()
			if not MainParameter.objects.filter(calculation=calc).exists():
				FieldsDBLoadData = total_fields.DBLoadData(calc)
				FieldsDBLoadData.load_data_in_db()

			serializer = self.serializer(calc)
			return Response(serializer.data)
		except Exception as e:
			return Response({'При расчетах произошла ошибка, код ошибки': traceback.format_exc()})

def model_formater_for_table(qs):
	'''форматирует данные из запроса для вывода в таблички'''
	fields = qs.model._meta.fields
	data = {field.name: [getattr(obj, field.name) for obj in qs] for field in fields if field.name not in ['calculation', 'id']}
	return data

class ProfitAndLossPlanView(APIView):
	permission_class = [IsAuthenticated]

	def get(self, request, pk):
		project = Project.objects.get(pk=pk, author=self.request.user)
		data = model_formater_for_table(ProfitAndLossPlan.objects.filter(calculation__project=project))
		return Response(data)

class CashFlowPlanView(generics.ListAPIView):
	permission_class = [IsAuthenticated]

	def get(self, request, pk):
		project = Project.objects.get(pk=pk, author=self.request.user)
		data = model_formater_for_table(CashFlowPlan.objects.filter(calculation__project=project))
		return Response(data)

class BalanceView(generics.ListAPIView):
	permission_class = [IsAuthenticated]

	def get(self, request, pk):
		project = Project.objects.get(pk=pk, author=self.request.user)
		data = model_formater_for_table(Balance.objects.filter(calculation__project=project))
		return Response(data)

class ResultFinancialAnalysView(generics.ListAPIView):
	permission_class = [IsAuthenticated]

	def get(self, request, pk):
		project = Project.objects.get(pk=pk, author=self.request.user)
		data = model_formater_for_table(ResultFinancialAnalys.objects.filter(calculation__project=project))
		return Response(data)


