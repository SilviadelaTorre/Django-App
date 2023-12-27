from django.contrib import admin
from . import models



class imageAdmin(admin.ModelAdmin):
    list_display = ["title", "photo"]


# Register your models here.
admin.site.register(models.Cruise)
admin.site.register(models.Destination)
admin.site.register(models.InfoRequest)
admin.site.register(models.Image, imageAdmin)





