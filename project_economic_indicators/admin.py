from django.contrib import admin
from . import models


admin.site.register(models.CapexObjectSetting)
admin.site.register(models.Capex)
admin.site.register(models.CapexObjectFile)