from django.contrib import admin
from . import models


class MagBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)


admin.site.register(models.MagBranch, MagBranchAdmin)
