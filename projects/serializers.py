import os
from rest_framework import serializers
from . import models


class DinamycFieldsModelSerializer(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		rename = kwargs.pop('rename', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)
			if rename is not None:
				self.fields['name']=self.fields.pop('variant_name')

class CurrencySerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Currency
		fields = ['name', 'id']

class CountrySerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Country
		fields = ['name', 'id']

class SegmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Segment
		fields = ['name', 'id', 'industry']

class IndustrySerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Industry
		fields = ['name', 'id',]

class AdditionalProjectInformationField(serializers.ModelSerializer):

	class Meta:
		model = models.AdditionalProjectInformation
		exclude = ['project', 'id']

class CopiedProjectField(serializers.ModelSerializer):

	class Meta:
		model = models.CopiedProject
		exclude = ['project', 'id']

class ProjectCompanyField(serializers.ModelSerializer):
	class Meta:
		model = models.ProjectCompany
		exclude = ['project', 'id']

class ProjectSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Project
		exclude = ['id', 'author', 'create_date', 'active', 'update_date']

class ProjectFileSerializer(serializers.ModelSerializer):
	file_size = serializers.SerializerMethodField()
	file_name = serializers.SerializerMethodField()
	file_format = serializers.SerializerMethodField()
	project = serializers.PrimaryKeyRelatedField(queryset=models.Project.objects.all(), write_only=True)
	
	class Meta:
		model = models.ProjectFile
		fields = '__all__'

	def get_file_size(self, obj):
		return os.stat(obj.file.path).st_size

	def get_file_name(self, obj):
		file_name = obj.file.name[:-4].split('/')[5]
		return file_name

	def get_file_format(self, obj):
		return obj.file.name[-3:]

class GetProjectSerializer(serializers.ModelSerializer):
	start_date = serializers.SerializerMethodField()

	class Meta:
		model = models.Project
		fields = ['name', 'create_date', 'start_date', 'comments', 'id']

	def get_start_date(self, obj):
		try:
			date = obj.calculation.variant_sales.sales_init.start_date
		except:
			date = None
		return date