from django.contrib import admin
from . import models

admin.site.register(models.OwnFund)
admin.site.register(models.Credit)
admin.site.register(models.LeasingContract)
admin.site.register(models.WorkingCapitalParameter)
admin.site.register(models.OwnFundVariant)
admin.site.register(models.CreditVariant)
admin.site.register(models.LeasingContractVariant)
