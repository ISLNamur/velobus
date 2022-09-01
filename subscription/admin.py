from django.contrib import admin
from . import models

admin.site.register(models.TrackModel)
admin.site.register(models.StopModel)
admin.site.register(models.SchoolModel)
admin.site.register(models.AvailableDateModel)
admin.site.register(models.ResponsibleModel)
admin.site.register(models.StudentModel)
