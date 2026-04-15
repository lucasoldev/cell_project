from django.contrib import admin
from . import models


class HostAdmin(admin.ModelAdmin):
    list_display = (
        'person',
        'short_address_display',
    )
    search_fields = ('person__full_name', 'full_address')
    raw_id_fields = ('person',)

    def short_address_display(self, obj):
        return obj.short_address
    short_address_display.short_description = 'Endereço'


admin.site.register(models.Host, HostAdmin)
