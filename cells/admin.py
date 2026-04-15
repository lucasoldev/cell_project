from django.contrib import admin
from . import models


class CellAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'area',
        'mag_branch',
        'cgsbc',
        'is_mag_cell',
        'created_at',
    )
    search_fields = ('name', 'cgsbc', 'area__color', 'mag_branch__name')
    list_filter = ('area', 'mag_branch', 'area__is_mag', 'created_at')
    #raw_id_fields = ('area', 'mag_branch')
    readonly_fields = ('created_at', 'updated_at', 'is_mag_cell')

    def is_mag_cell(self, obj):
        """Indica se a célula é da área MAG"""
        return obj.area.is_mag if obj.area else False
    is_mag_cell.boolean = True
    is_mag_cell.short_description = 'É MAG?'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('area', 'mag_branch')

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'area', 'cgsbc')
        }),
        ('Ramificação MAG', {
            'fields': ('mag_branch',),
            'description': 'Apenas para células da área MAG (Vermelha)'
        }),
        ('Observações', {
            'fields': ('notes',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(models.Cell, CellAdmin)