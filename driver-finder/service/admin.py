from django.contrib import admin
from service import models
# Register your models here.

admin.site.register(models.Location)
admin.site.register(models.Mention)

