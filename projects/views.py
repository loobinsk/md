from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from project_calculations.models import Calculation
from . import models, choices
from . import serializers, permissions


class GetProjectsView(generics.ListAPIView):
	serializer_class = serializers.GetProjectSerializer
	filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['name']
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			return models.Project.objects.all()
		else:
			return models.Project.objects.filter(author=user, active=True)

class CreateNewProject(APIView):
	'''создает проект и все его дочерние таблицы
	возвращает айдишник созданного объекта'''
	permission_classes = [IsAuthenticated]

	def post(self, request):
		try:
			data = {}
			new_project = models.Project.objects.create(author=self.request.user, comments='')
			add_project_inf = models.AdditionalProjectInformation.objects.create(project=new_project)
			copy_project = models.CopiedProject.objects.create(project=new_project)
			project_company= models.ProjectCompany.objects.create(project=new_project)
			calculation = Calculation.objects.create(project=new_project)
			try:
				date = new_project.calculation.variant_sales.sales_init.start_date
			except:
				date = None
			data = {'id': new_project.id, 
					'name':new_project.name, 
					'create_date':new_project.create_date, 
					'start_date':date, 
					'comments':new_project.comments,}
			return Response(data, status=status.HTTP_200_OK)
		except Exception as err:
			return Response({'errors': str(err)}, status=status.HTTP_400_BAD_REQUEST)

class GetProjectNameView(APIView):

	def get(self, request, pk):
		project = get_object_or_404(models.Project, pk=pk, author=request.user)
		data = {'name': project.name}
		return Response(data)


class GetProjectsEnumsView(APIView):

	def get(self, request):
		data = {}
		industries = models.Industry.objects.all()
		serializer = serializers.IndustrySerializer(industries, many=True)
		currencies = models.Currency.objects.all()
		serializer2 = serializers.CurrencySerializer(currencies, many=True)
		countries = models.Country.objects.all()
		serializer3 = serializers.CountrySerializer(countries, many=True)
		data['industries'] = serializer.data
		data['currencies'] = serializer2.data
		data['countries'] = serializer3.data
		data['financing_type'] = choices.get_true_list_enums(choices.FINANCING_TYPE)
		data['currency_multiplication'] = choices.get_true_list_enums(choices.CURRENCY_MULTIPLICATION)
		data['time_detalizations'] = choices.get_true_list_enums(choices.TIME_DETALIZATIONS)
		return Response(data, status=status.HTTP_200_OK)


class ProjectUpdate(generics.RetrieveUpdateAPIView):
	serializer_class = serializers.ProjectSerializer

	def get_queryset(self):
		user = self.request.user
		return models.Project.objects.filter(author=user)

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=True)

		if serializer.is_valid():
			serializer.save()
			if instance.init_industry_main!=instance.industry_main:
				instance.industry_segments.clear()
			return Response(serializer.data)

class AdditionalProjectInformationUpdate(generics.RetrieveUpdateAPIView):
	queryset = models.AdditionalProjectInformation.objects.all()
	serializer_class = serializers.AdditionalProjectInformationField

	def get_object(self):
		project = models.Project.objects.get(pk=self.kwargs['pk'], author=self.request.user)
		queryset = self.filter_queryset(self.get_queryset())
		obj = queryset.get(project=project)
		return obj

class CopiedProjectUpdate(generics.RetrieveUpdateAPIView):
	queryset = models.CopiedProject.objects.all()
	serializer_class = serializers.CopiedProjectField

	def get_object(self):
		project = models.Project.objects.get(pk=self.kwargs['pk'], author=self.request.user)
		queryset = self.filter_queryset(self.get_queryset())
		obj = queryset.get(project=project)
		return obj

class ProjectCompanyUpdate(generics.RetrieveUpdateAPIView):
	queryset = models.ProjectCompany.objects.all()
	serializer_class = serializers.ProjectCompanyField

	def get_object(self):
		project = models.Project.objects.get(pk=self.kwargs['pk'], author=self.request.user)
		queryset = self.filter_queryset(self.get_queryset())
		obj = queryset.get(project=project)
		return obj

class FileCreateView(generics.ListCreateAPIView):
	serializer_class = serializers.ProjectFileSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['project']

	def get_queryset(self):
		user = self.request.user
		return models.ProjectFile.objects.filter(project__author=user)

class FileDeleteView(generics.DestroyAPIView):
	queryset = models.ProjectFile.objects.all()
	serializer_class = serializers.ProjectFileSerializer
	permission_classes = [permissions.IsOwner]