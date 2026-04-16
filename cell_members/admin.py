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
<<<<<<< HEAD
    readonly_fields = ('created_at', 'updated_at',)

    fieldsets = (
        ('Member Information', {
            'fields': ('member', 'cell', 'role')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Period', {
            'fields': ('start_date', 'end_date',),
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('System Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
=======
>>>>>>> bfda95313dc2068c3e959514fde0f4313aa074ea

    def member_name_display(self, obj):
        return obj.member_name
    member_name_display.short_description = 'Membro'
    member_name_display.admin_order_field = 'member__person__full_name'

    def role_display(self, obj):
        """Exibe 'Membro' quando role for nulo"""
<<<<<<< HEAD
        return obj.role_display if hasattr(obj, 'role_display') else (obj.role.title if obj.role else 'Membro')
=======
        return obj.role_display
>>>>>>> bfda95313dc2068c3e959514fde0f4313aa074ea
    role_display.short_description = 'Função'
    role_display.admin_order_field = 'role__title'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
<<<<<<< HEAD
            'member__person', 'cell__area', 'role'
        )


admin.site.register(models.CellMember, CellMemberAdmin)
=======
            'member__person', 'cell', 'role'
        )


admin.site.register(models.CellMember, CellMemberAdmin)
>>>>>>> bfda95313dc2068c3e959514fde0f4313aa074ea
