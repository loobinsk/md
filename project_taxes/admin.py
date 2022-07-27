from django.contrib import admin
from . import models


admin.site.register(models.TaxPrm)
admin.site.register(models.TaxPrmTemplate)
admin.site.register(models.DiscountRate)