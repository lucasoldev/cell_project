from django.contrib import admin
from . import models


class CellMemberAdmin(admin.ModelAdmin):
    """
    Admin configuration for CellMember model.
    Role is optional - leave empty for regular members.
    """

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
        'cell',
        'start_date',
    )
    raw_id_fields = ('member', 'cell', 'role')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Member Information', {
            'fields': ('member', 'cell')
        }),
        ('Leadership Role', {
            'fields': ('role',),
            'description': 'Optional. Leave empty for regular members without leadership role.'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Period', {
            'fields': ('start_date', 'end_date'),
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('System Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def member_name_display(self, obj):
        """Displays the member's full name"""
        return obj.member_name
    member_name_display.short_description = 'Member'
    member_name_display.admin_order_field = 'member__person__full_name'

    def role_display(self, obj):
        """Displays 'Membro' when role is null, otherwise the role title"""
        return obj.role_display
    role_display.short_description = 'Role'
    role_display.admin_order_field = 'role__title'

    def get_queryset(self, request):
        """Optimizes queryset with select_related for foreign keys"""
        return super().get_queryset(request).select_related(
            'member__person',
            'cell__area',
            'role'
        )


admin.site.register(models.CellMember, CellMemberAdmin)
