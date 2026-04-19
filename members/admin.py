from django.contrib import admin

from . import models


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'person',
        'is_active',
        'entry_date',
    )
    search_fields = ('person__full_name',)
    list_filter = ('is_active', 'entry_date')
    raw_id_fields = ('person',)


admin.site.register(models.Member, MemberAdmin)
