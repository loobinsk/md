from rest_framework import serializers
from . import models
import copy, os

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

class CapexSerializer(serializers.ModelSerializer):
	object_settings = CapexObjectSettingsSerializer(read_only=True)
	
	class Meta:
		model = models.Capex
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super().__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)