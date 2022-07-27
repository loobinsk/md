from django.contrib import admin
from . import models

admin.site.register(models.Currency)
admin.site.register(models.Country)
admin.site.register(models.Industry)
admin.site.register(models.Segment)
admin.site.register(models.Project)
admin.site.register(models.AdditionalProjectInformation)
admin.site.register(models.CopiedProject)
admin.site.register(models.ProjectCompany)
admin.site.register(models.ProjectFile)
admin.site.register(models.ProjectTemplate)