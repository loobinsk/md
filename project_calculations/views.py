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
from .calc_funcs import balance, results
from .models import Calculation, ResultFinancialAnalys, Balance
from .models import ProfitAndLossPlan, CashFlowPlan
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
		ResultFinancialAnalys.objects.all().delete()
		Balance.objects.all().delete()
		CashFlowPlan.objects.all().delete()
		ProfitAndLossPlan.objects.all().delete()

		calc = Calculation.objects.all().first()
		PL = profit_and_loss.ProfitAndLossPlan(calc)
		FL = flow_funds.FlowFunds(calc)
		dataFL = FL.add_data_in_db()
		dataPL = PL.add_data_in_db()

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

class CalcResultsView(generics.RetrieveAPIView):
	serializer_class= serializers.CalculationResultSerializer
	queryset = Calculation.objects.all()
	permission_classes = [IsAuthenticated]

	def get_object(self):
		project = Project.objects.get(pk=self.kwargs['pk'], author=self.request.user)
		queryset = self.filter_queryset(self.get_queryset())
		obj = queryset.get(project=project)
		return obj

class ProfitAndLossPlanView(generics.ListAPIView):
	serializer_class= serializers.ProfitAndLossSerializer
	queryset = ProfitAndLossPlan.objects.all()
	permission_classes = [IsAuthenticated]
	pagination_class = None

	def get_queryset(self):
		project = Project.objects.get(pk=self.kwargs['pk'], author=self.request.user)
		return ProfitAndLossPlan.objects.filter(calculation__project=project)

class CashFlowPlanView(generics.ListAPIView):
	serializer_class= serializers.CashFlowPlanSerializer
	permission_class = [IsAuthenticated]

	def get_queryset(self):
		project = Project.objects.get(pk=self.kwargs['pk'], author=self.request.user)
		return CashFlowPlan.objects.filter(calculation__project=project)

class BalanceView(generics.ListAPIView):
	serializer_class= serializers.BalanceSerializer
	permission_class = [IsAuthenticated]

	def get_queryset(self):
		project = Project.objects.get(pk=self.kwargs['pk'], author=self.request.user)
		return Balance.objects.filter(calculation__project=project)

class ResultFinancialAnalysView(generics.ListAPIView):
	serializer_class= serializers.ResultFinancialAnalysSerializer
	permission_class = [IsAuthenticated]

	def get_queryset(self):
		project = Project.objects.get(pk=self.kwargs['pk'], author=self.request.user)
		return ResultFinancialAnalys.objects.filter(calculation__project=project)

class CalculationView1(APIView):

	def post(self, request):
		ResultFinancialAnalys.objects.all().delete()
		Balance.objects.all().delete()
		CashFlowPlan.objects.all().delete()
		ProfitAndLossPlan.objects.all().delete()

		calc = Calculation.objects.all().first()
		PL = profit_and_loss.ProfitAndLossPlan(calc)
		FL = flow_funds.FlowFunds(calc)
		BL = balance.BalanceCalc(calc)
		RS = results.FinancialAnalysisResult(calc)
		PL.add_data_in_db()
		FL.add_data_in_db()
		BL.add_data_in_db()
		RS.add_data_in_db()
		return Response('Все отлично')


