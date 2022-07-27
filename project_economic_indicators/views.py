from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from projects.models import Project
from projects import choices

from . import models, serializers
from . import permissions


class CopyCapexView(APIView):
	def get_object(self, pk):
		return get_object_or_404(models.ProjectCapex, pk=pk)

	def get_files(self, capex):
		return capex.object_settings.files.all()

	def post(self, request, pk):
		project_capex = self.get_object(pk)
		files = self.get_files(project_capex)
		print(files)
		if project_capex.project.author==request.user:
			capex_object = project_capex.object_settings
			project_capex.id = None
			project_capex.variant_name = f'Copy {project_capex.variant_name}'
			project_capex.save()
			capex_object.id = None
			capex_object.capex = project_capex
			capex_object.save()
			print(files)
			for file in files.all():
				file.id=None
				file._object=capex_object
				file.save()
			serializer=serializers.CapexSerializer(project_capex)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, status=status.HTTP_400_BAD_REQUEST)

class CapexEnums(APIView):
	def get(self, request):
		data = {}
		data['rates'] = choices.get_true_list_enums(choices.RATES)
		return Response(data, status=status.HTTP_200_OK)



class CapexListView(generics.ListCreateAPIView):
	serializer_class = serializers.CapexSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = '__all__'
	permission_classes = [permissions.IsOwnerCapex, IsAuthenticated]
	pagination_class=None

	def create(self, request, *args, **kwargs):
		user = request.user
		project = get_object_or_404(Project, pk=request.data['project'])
		if project.author==user:
			request.data.pop('project')
			obj = models.Capex.objects.create(project=project)
			object = models.CapexObjectSetting.objects.create(capex=obj)
			capex_serializer = serializers.CapexSerializer(obj)
			return Response(capex_serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'detail': "Вы не имеете доступ к созданию этого объекта к чужому проекту."}, status=status.HTTP_400_BAD_REQUEST)

	def get_queryset(self):
		user = self.request.user
		return models.Capex.objects.filter(project__author=user)


class CapexDetailView(generics.RetrieveUpdateAPIView):
	queryset = models.Capex.objects.all()
	serializer_class = serializers.CapexSerializer
	permission_classes = [permissions.IsOwnerCapex, IsAuthenticated]

class CapexObjectDetailView(generics.RetrieveUpdateAPIView):
	queryset = models.CapexObjectSetting.objects.all()
	serializer_class = serializers.CapexObjectSettingsSerializer

	def get_object(self):
		capex = get_object_or_404(models.Capex, pk=self.kwargs['pk'], project__author=self.request.user)
		queryset = self.filter_queryset(self.get_queryset())
		obj = queryset.get(capex=capex)
		return obj

class CapexObjectFileListView(generics.ListCreateAPIView):
	serializer_class = serializers.CapexObjectFilesSerializer
	permission_classes = [permissions.IsOwnerFile, IsAuthenticated]
	pagination_class=None

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = request.user
		object = get_object_or_404(models.CapexObjectSetting, pk=request.data['_object'])
		if object.capex.project.author==user:
			self.perform_create(serializer)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
		else:
			return Response({'detail': "Вы не имеете доступ к созданию этого файла к чужому объекту кап. расходов."}, 
							status=status.HTTP_400_BAD_REQUEST)

	def get_queryset(self):
		user = self.request.user
		return models.CapexObjectFile.objects.filter(_object__capex__project__author=user)

class CapexObjectFileDetailView(generics.DestroyAPIView):
	queryset = models.CapexObjectFile.objects.all()
	serializer_class = serializers.CapexObjectFilesSerializer
	permission_classes = [permissions.IsOwnerFile, IsAuthenticated]


