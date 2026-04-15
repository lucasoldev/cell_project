from django.contrib import admin
from . import models


class AreaAdmin(admin.ModelAdmin):
    list_display = ('color', 'is_mag',)
    search_fields = ('color',)


admin.site.register(models.Area, AreaAdmin)
