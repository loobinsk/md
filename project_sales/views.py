from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from projects.models import Project
from projects import choices

from . import models, permissions
from . import serializers


class SalesInitListView(generics.ListCreateAPIView):
	serializer_class = serializers.SalesInitSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = '__all__'
	permission_classes = [IsAuthenticated]
	pagination_class=None

	def create(self, request, *args, **kwargs):
		user = request.user
		project = get_object_or_404(Project, pk=request.data['project'])
		if project.author==user:
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'detail': "Вы не имеете доступ к созданию этого объекта к чужому проекту."}, status=status.HTTP_400_BAD_REQUEST)

	def get_queryset(self):
		user = self.request.user
		return models.SalesInit.objects.filter(project__author=user)

class SalesInitCopyView(APIView):

	def post(self, request, pk):
		sales_init = get_object_or_404(models.SalesInit, pk=pk)
		if sales_init.project.author==request.user:
			sales_init.id = None
			sales_init.variant_name = f'Copy {sales_init.variant_name}'
			sales_init.save()
			serializer=serializers.SalesInitSerializer(sales_init)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, 
							status=status.HTTP_400_BAD_REQUEST)

class SalesInitDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.SalesInit.objects.all()
	serializer_class = serializers.SalesInitSerializer
	permission_classes = [permissions.IsOwner, IsAuthenticated]

class SalesInitEnums(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		data = {}
		data['product_units'] = choices.get_true_list_enums(choices.UNITS)
		data['rates'] = choices.get_true_list_enums(choices.RATES)
		data['value_indexation_period'] = choices.get_true_list_enums(choices.VALUE_INDEXATION_PERIOD)
		return Response(data, status=status.HTTP_200_OK)

class OpexsEnums(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		data = {}
		data['cost_types_by_economic_grouping'] = choices.get_true_list_enums(choices.TYPES_BUSINESS_ACTIVITY_COSTS)
		data['fixed_asset_lease_payment'] = choices.get_true_list_enums(choices.FIXED_ASSET_LEASE_PAYMENT)
		data['rates'] = choices.get_true_list_enums(choices.RATES)
		return Response(data, status=status.HTTP_200_OK)

class OpexVariantListCreateView(generics.ListCreateAPIView):
	serializer_class = serializers.OpexVariantSerializer
	pagination_class =None

	def create(self, request, *args, **kwargs):
		user = request.user
		project = get_object_or_404(Project, pk=request.data['project'])
		if project.author==user:
			variant = models.OpexVariant.objects.create(project=project)
			opex = models.Opex.objects.create(variant=variant)
			sr = serializers.OpexVariantSerializer(variant)
			return Response(sr.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'detail': "Вы не имеете доступ к созданию этого объекта к чужому проекту."}, 
							status=status.HTTP_400_BAD_REQUEST)

	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		return models.OpexVariant.objects.filter(project__author=user)

class OpexVariantDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.OpexVariant.objects.all()
	serializer_class = serializers.OpexVariantSerializer
	permission_classes = [permissions.IsOwner, IsAuthenticated]

class OpexVariantCopyView(APIView):
	def post(self, request, pk):
		opex_variant = get_object_or_404(models.OpexVariant, pk=pk)
		opexs = opex_variant.opexs.all()
		print(opexs)
		if opex_variant.project.author==request.user:
			opex_variant.id = None
			opex_variant.variant_name = f'Copy {opex_variant.variant_name}'
			opex_variant.save()
			variant_serializer=serializers.OpexVariantSerializer(opex_variant)
			for opex in opexs:
				opex.id = None
				opex.variant=opex_variant
				opex.save()
				opex_serializer = serializers.OpexSerializer(opex)
			return Response(variant_serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, 
							status=status.HTTP_400_BAD_REQUEST)

class OpexListCreateView(generics.ListCreateAPIView):
	serializer_class = serializers.OpexSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = '__all__'
	pagination_class =None

	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		return models.Opex.objects.filter(variant__project__author=user)

class OpexDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Opex.objects.all()
	serializer_class = serializers.OpexSerializer
	permission_classes = [permissions.CapexIsOwner, IsAuthenticated]

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		data={'variant_expenses': instance.variant.get_total_opexs()}
		self.perform_destroy(instance)
		return Response(data)

	def retrieve(self, request, pk=None):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		data={'opex': serializer.data,
			'variant_expenses': instance.variant.get_total_opexs()}
		return Response(data)

class OpexCopyView(APIView):
	def post(self, request, pk):
		opex = get_object_or_404(models.Opex, pk=pk)
		opex_variant = opex.variant
		print(opex_variant)
		if opex.variant.project.author==request.user:
			opex.id = None
			opex.name = f'Copy {opex.name}'
			opex.save()
			opex_serializer=serializers.OpexSerializer(opex)
			data={}
			data['opex']=dict(opex_serializer.data)
			data['variant_expenses']=opex.variant.get_total_opexs()
			return Response(data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, 
							status=status.HTTP_400_BAD_REQUEST)