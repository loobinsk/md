from django.contrib import admin
from . import models


admin.site.register(models.SalesInit)
admin.site.register(models.Opex)
admin.site.register(models.OpexVariant)