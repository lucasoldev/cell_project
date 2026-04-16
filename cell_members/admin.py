from django.contrib import admin
from . import models


class CellMemberAdmin(admin.ModelAdmin):
    list_display = (
        'member_name_display',
        'cell',
        'role_display',
        'is_active',
        'start_date',
        'end_date',
    )
    search_fields = (
        'member__person__full_name',
        'cell__name',
        'role__title',
    )
    list_filter = (
        'is_active',
        'role',
        'cell__area',
        'start_date',
    )
    raw_id_fields = ('member', 'cell', 'role')
    date_hierarchy = 'start_date'

    def member_name_display(self, obj):
        return obj.member_name
    member_name_display.short_description = 'Membro'
    member_name_display.admin_order_field = 'member__person__full_name'

    def role_display(self, obj):
        """Exibe 'Membro' quando role for nulo"""
        return obj.role_display
    role_display.short_description = 'Função'
    role_display.admin_order_field = 'role__title'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'member__person', 'cell', 'role'
        )


admin.site.register(models.CellMember, CellMemberAdmin)