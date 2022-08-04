from django.shortcuts import get_object_or_404
from rest_framework import generics, filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from projects import choices
from projects import models as project_models
from . import models, permissions
from . import serializers


class OwnFundVariantCreateView(generics.ListCreateAPIView):
	serializer_class = serializers.OwnFundVariantSerializer
	pagination_class = None

	def create(self, request, *args, **kwargs):
		user = request.user
		project = get_object_or_404(project_models.Project, pk=request.data['project'])
		if project.author==user:
			variant = models.OwnFundVariant.objects.create(project=project)
			sr = serializers.OwnFundVariantSerializer(variant)
			return Response(sr.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'detail': "Вы не имеете доступ к созданию этого объекта к чужому проекту."}, 
							status=status.HTTP_400_BAD_REQUEST)

	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		return models.OwnFundVariant.objects.filter(project__author=user)

class OwnFundVariantDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.OwnFundVariant.objects.all()
	serializer_class = serializers.OwnFundVariantSerializer
	permission_classes = [permissions.IsOwner, IsAuthenticated]

class OwnFundVariantCopyView(APIView):
	def post(self, request, pk):
		own_fund_variant = get_object_or_404(models.OwnFundVariant, pk=pk)
		own_funds = own_fund_variant.own_funds.all()
		print(own_funds)
		if own_fund_variant.project.author==request.user:
			own_fund_variant.id = None
			own_fund_variant.variant_name = f'Copy {own_fund_variant.variant_name}'
			own_fund_variant.save()
			variant_serializer=serializers.OwnFundVariantSerializer(own_fund_variant)
			for own_fund in own_funds:
				own_fund.id = None
				own_fund.variant=own_fund_variant
				own_fund.save()
			return Response(variant_serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."},
							status=status.HTTP_400_BAD_REQUEST)

class OwnFundListView(generics.ListCreateAPIView):
	serializer_class = serializers.OwnFundSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = '__all__'
	pagination_class = None

	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		return models.OwnFund.objects.filter(variant__project__author=user)

class OwnFundDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.OwnFund.objects.all()
	serializer_class = serializers.OwnFundSerializer
	permission_classes = [permissions.ObjectIsOwner, IsAuthenticated]

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		data={'variant_own_funds': instance.variant.get_total_own_funds()}
		self.perform_destroy(instance)
		return Response(data)

	def retrieve(self, request, pk=None):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		data={'own_fund': serializer.data, 
			'variant_own_funds': instance.variant.get_total_own_funds()}
		return Response(data)

class OwnFundCopyView(APIView):
	def post(self, request, pk):
		own_fund = get_object_or_404(models.OwnFund, pk=pk)
		own_fund_variant = own_fund.variant
		print(own_fund_variant)
		if own_fund.variant.project.author==request.user:
			own_fund.id = None
			own_fund.name = f'Copy {own_fund.name}'
			own_fund.save()
			own_fund_serializer=serializers.OwnFundSerializer(own_fund)
			data = {'own_fund': own_fund_serializer.data,
					'variant_own_funds': own_fund.variant.get_total_own_funds()
				}
			return Response(data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, 
							status=status.HTTP_400_BAD_REQUEST)

class CreditEnums(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		data = {}
		data['calculation_type'] = choices.get_true_list_enums(choices.CALCULATION_TYPE)
		return Response(data, status=status.HTTP_200_OK)

class CreditVariantCreateView(generics.ListCreateAPIView):
	serializer_class = serializers.CreditVariantSerializer
	pagination_class = None

	def create(self, request, *args, **kwargs):
		user = request.user
		project = get_object_or_404(project_models.Project, pk=request.data['project'])
		if project.author==user:
			variant = models.CreditVariant.objects.create(project=project)
			sr = serializers.CreditVariantSerializer(variant)
			return Response(sr.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'detail': "Вы не имеете доступ к созданию этого объекта к чужому проекту."}, 
							status=status.HTTP_400_BAD_REQUEST)

	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		return models.CreditVariant.objects.filter(project__author=user)

class CreditVariantDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.CreditVariant.objects.all()
	serializer_class = serializers.CreditVariantSerializer
	permission_classes = [permissions.IsOwner, IsAuthenticated]

class CreditVariantCopyView(APIView):
	def post(self, request, pk):
		credit_variant = get_object_or_404(models.CreditVariant, pk=pk)
		credits = credit_variant.credits.all()
		print(credits)
		if credit_variant.project.author==request.user:
			credit_variant.id = None
			credit_variant.variant_name = f'Copy {credit_variant.variant_name}'
			credit_variant.save()
			variant_serializer=serializers.CreditVariantSerializer(credit_variant)
			for credit in credits:
				credit.id = None
				credit.variant=credit_variant
				credit.save()
			return Response(variant_serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."},
							status=status.HTTP_400_BAD_REQUEST)

class CreditsListView(generics.ListCreateAPIView):
	queryset = models.Credit.objects.all()
	serializer_class = serializers.CreditSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = '__all__'
	pagination_class = None

	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		return models.Credit.objects.filter(variant__project__author=user)

def get_credit_shares(variant):
	credits = variant.credits.all()
	data = {credit.id: credit.credit_share() for credit in credits}
	return data

class CreditDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Credit.objects.all()
	serializer_class = serializers.CreditSerializer
	permission_classes = [permissions.ObjectIsOwner, IsAuthenticated]

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		data={'variant_total_contributions': instance.variant.total_contributions(),
			'credit_shares': get_credit_shares(instance.variant)}
		self.perform_destroy(instance)
		return Response(data)

	def retrieve(self, request, pk=None):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		shares = get_credit_shares(instance.variant)
		print(get_credit_shares(instance.variant))
		data={'credit': serializer.data, 
			'variant_total_contributions': instance.variant.total_contributions(),
			'credit_shares': shares}
		return Response(data)

class CreditCopyView(APIView):
	def post(self, request, pk):
		credit = get_object_or_404(models.Credit, pk=pk)
		credit_variant = credit.variant
		print(credit_variant)
		if credit.variant.project.author==request.user:
			credit.id = None
			credit.name = f'Copy {credit.name}'
			credit.save()
			credit_serializer=serializers.CreditSerializer(credit)
			data = {'credit': credit_serializer.data,
					'variant_total_contributions': credit.variant.total_contributions(),
					'credit_shares': get_credit_shares(credit.variant)
				}
			return Response(data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, 
							status=status.HTTP_400_BAD_REQUEST)

class LeasingEnums(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		data = {}
		data['rates'] = choices.get_true_list_enums(choices.RATES)
		return Response(data, status=status.HTTP_200_OK)

class LeasingVariantCreateView(generics.ListCreateAPIView):
	serializer_class = serializers.LeasingContractVariantSerializer
	pagination_class = None

	def create(self, request, *args, **kwargs):
		user = request.user
		project = get_object_or_404(project_models.Project, pk=request.data['project'])
		if project.author==user:
			variant = models.LeasingContractVariant.objects.create(project=project)
			sr = serializers.LeasingContractVariantSerializer(variant)
			return Response(sr.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'detail': "Вы не имеете доступ к созданию этого объекта к чужому проекту."}, 
							status=status.HTTP_400_BAD_REQUEST)

	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		return models.LeasingContractVariant.objects.filter(project__author=user)

class LeasingVariantDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.LeasingContractVariant.objects.all()
	serializer_class = serializers.LeasingContractVariantSerializer
	permission_classes = [permissions.IsOwner, IsAuthenticated]

class LeasingVariantCopyView(APIView):
	def post(self, request, pk):
		leasing_variant = get_object_or_404(models.LeasingContractVariant, pk=pk)
		leasings = leasing_variant.leasings.all()
		print(leasings)
		if leasing_variant.project.author==request.user:
			leasing_variant.id = None
			leasing_variant.variant_name = f'Copy {leasing_variant.variant_name}'
			leasing_variant.save()
			variant_serializer=serializers.LeasingContractVariantSerializer(leasing_variant)
			for leasing in leasings:
				leasing.id = None
				leasing.variant=leasing_variant
				leasing.save()
			return Response(variant_serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."},
							status=status.HTTP_400_BAD_REQUEST)

class LeasingListView(generics.ListCreateAPIView):
	serializer_class = serializers.LeasingContractSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = '__all__'
	pagination_class = None

	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		return models.LeasingContract.objects.filter(variant__project__author=user)

class LeasingDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.LeasingContract.objects.all()
	serializer_class = serializers.LeasingContractSerializer
	permission_classes = [permissions.ObjectIsOwner, IsAuthenticated]

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		data={'variant_total_pays': instance.variant.total_pays()}
		self.perform_destroy(instance)
		return Response(data)

	def retrieve(self, request, pk=None):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		data={'leasing': serializer.data, 
			'variant_total_pays': instance.variant.total_pays()}
		return Response(data)

class LeasingCopyView(APIView):
	def post(self, request, pk):
		leasing = get_object_or_404(models.LeasingContract, pk=pk)
		leasing_variant = leasing.variant
		print(leasing_variant)
		if leasing.variant.project.author==request.user:
			leasing.id = None
			leasing.name = f'Copy {leasing.name}'
			leasing.save()
			serializer=serializers.LeasingContractSerializer(leasing)
			data = {'leasing': serializer.data,
					'variant_total_pays': leasing.variant.total_pays()
				}
			return Response(data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, 
							status=status.HTTP_400_BAD_REQUEST)



class WorkingCapitalParameterListView(generics.ListCreateAPIView):
	serializer_class = serializers.WorkingCapitalParameterSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = '__all__'
	permission_classes = [IsAuthenticated]
	pagination_class=None

	def create(self, request, *args, **kwargs):
		user = request.user
		project = get_object_or_404(project_models.Project, pk=request.data['project'])
		if project.author==user:
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'detail': "Вы не имеете доступ к созданию этого объекта к чужому проекту."}, 
							status=status.HTTP_400_BAD_REQUEST)

	def get_queryset(self):
		user = self.request.user
		return models.WorkingCapitalParameter.objects.filter(project__author=user)

class WorkingCapitalParameterCopyView(APIView):

	def post(self, request, pk):
		working_capital_parameter = get_object_or_404(models.WorkingCapitalParameter, pk=pk)
		if working_capital_parameter.project.author==request.user:
			working_capital_parameter.id = None
			working_capital_parameter.variant_name = f'Copy {working_capital_parameter.variant_name}'
			working_capital_parameter.save()
			serializer=serializers.WorkingCapitalParameterSerializer(working_capital_parameter)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, 
							status=status.HTTP_400_BAD_REQUEST)

class WorkingCapitalParameterDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.WorkingCapitalParameter.objects.all()
	serializer_class = serializers.WorkingCapitalParameterSerializer
	permission_classes = [permissions.IsOwner, IsAuthenticated]

