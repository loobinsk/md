from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from . import models, permissions
from . import serializers
from projects import choices
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class TaxPrmListView(generics.ListCreateAPIView):
	serializer_class = serializers.TaxPrmSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = '__all__'
	pagination_class = None

	def get_queryset(self):
		user = self.request.user
		return models.TaxPrm.objects.filter(project__author=user)

class TaxPrmGetUpdateView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.TaxPrm.objects.all()
	serializer_class = serializers.TaxPrmSerializer
	permission_classes = [permissions.IsOwner]

class TaxPrmEnums(APIView):
	def get(self, request):
		data = {}
		data['tax_simulation'] = choices.get_true_list_enums(choices.TAX_SIMULATION)
		data['tax_min_burden_base'] = choices.get_true_list_enums(choices.TAX_MIN_BURDEN_BASE)
		data['calculation_frequency'] = choices.get_true_list_enums(choices.TIME_DETALIZATIONS)
		return Response(data, status=status.HTTP_200_OK)

class CopyTaxPrm(APIView):

	def get_object(self, pk):
		return get_object_or_404(models.TaxPrm, pk=pk)

	def post(self, request, pk):
		tax_prm = self.get_object(pk)
		if tax_prm.project.author==request.user:
			tax_prm.id = None
			tax_prm.variant_name = f'Copy {tax_prm.variant_name}'
			tax_prm.save()
			serializer=serializers.TaxPrmSerializer(tax_prm)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, status=status.HTTP_400_BAD_REQUEST)

class DiscountRateCreateListView(generics.ListCreateAPIView):
	serializer_class = serializers.DiscountRateSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = '__all__'
	pagination_class = None

	def get_queryset(self):
		user = self.request.user
		return models.DiscountRate.objects.filter(project__author=user)

class DiscountRateGetUpdateView(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.DiscountRate.objects.all()
	serializer_class = serializers.DiscountRateSerializer
	permission_classes = [permissions.IsOwner]

class DiscountRateCopyView(APIView):
	def post(self, request, pk):
		discount_rate = get_object_or_404(models.DiscountRate, pk=pk)
		if discount_rate.project.author==request.user:
			discount_rate.id = None
			discount_rate.variant_name = f'Copy {discount_rate.variant_name}'
			discount_rate.save()
			serializer=serializers.DiscountRateSerializer(discount_rate)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, status=status.HTTP_400_BAD_REQUEST)