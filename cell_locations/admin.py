from django.contrib import admin

from . import models


class CellLocationAdmin(admin.ModelAdmin):
    list_display = (
        'cell',
        'host',
        'short_address_display',
        'is_active',
        'created_at',
    )
    search_fields = ('cell__name', 'host__person__full_name', 'address')
    list_filter = ('is_active', 'cell__area', 'created_at')
    raw_id_fields = ('cell', 'host')

    def short_address_display(self, obj):
        return obj.short_address
    short_address_display.short_description = 'Endereço'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'cell', 'host__person'
        )


admin.site.register(models.CellLocation, CellLocationAdmin)
