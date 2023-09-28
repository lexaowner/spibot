from django.contrib import admin
from . import models

admin.site.register(models.Region)
admin.site.register(models.House)
admin.site.register(models.Street)
admin.site.register(models.District)
