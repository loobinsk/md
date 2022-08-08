import copy, os
from rest_framework import serializers
from . import models
from projects.serializers import DinamycFieldsModelSerializer

class CapexObjectFilesSerializer(serializers.ModelSerializer):
	file_size = serializers.SerializerMethodField()
	file_name = serializers.SerializerMethodField()
	file_format = serializers.SerializerMethodField()
	class Meta:
		model = models.CapexObjectFile
		fields = '__all__'

	def get_file_size(self, obj):
		return os.stat(obj.file.path).st_size

	def get_file_name(self, obj):
		return obj.file.name[:-4].split('/')[5]

	def get_file_format(self, obj):
		return obj.file.name[-3:]

class CapexObjectSettingsSerializer(serializers.ModelSerializer):
	files = CapexObjectFilesSerializer(read_only=True, many=True)
	class Meta:
		model = models.CapexObjectSetting
		fields = '__all__'

class CapexSerializer(DinamycFieldsModelSerializer):
	object_settings = CapexObjectSettingsSerializer(read_only=True)
	active = serializers.SerializerMethodField(read_only=True)
	
	class Meta:
		model = models.Capex
		fields='__all__'

	def get_active(self, obj):
		if obj.start_date and obj.end_date:
			return True
		else:
			return False