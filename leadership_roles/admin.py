from django.contrib import admin

from . import models


class LeadershipRoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    search_fields = ('title',)

admin.site.register(models.LeadershipRole, LeadershipRoleAdmin)
