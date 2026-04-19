from django.contrib import admin

from . import models


class MemberMinistryAdmin(admin.ModelAdmin):
    """
    Admin configuration for MemberMinistry model.
    Tracks member participation in church ministries.
    """

    list_display = (
        'member_name_display',
        'ministry_name_display',
        'is_active',
        'start_date',
        'end_date',
        'duration_days_display',
    )
    search_fields = (
        'member__person__full_name',
        'ministry__name',
    )
    list_filter = (
        'is_active',
        'ministry',
        'start_date',
    )
    raw_id_fields = ('member', 'ministry')
    date_hierarchy = 'start_date'
    readonly_fields = (
        'created_at',
        'updated_at',
        'duration_days_display',
        'status_display',
    )

    fieldsets = (
        ('Participation Information', {
            'fields': ('member', 'ministry', 'is_active', 'status_display')
        }),
        ('Period', {
            'fields': ('start_date', 'end_date', 'duration_days_display'),
        }),
        ('Notes', {
            'fields': ('notes',),
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

    def ministry_name_display(self, obj):
        """Displays the ministry name"""
        return obj.ministry_name
    ministry_name_display.short_description = 'Ministry'
    ministry_name_display.admin_order_field = 'ministry__name'

    def duration_days_display(self, obj):
        """Displays the duration in days"""
        return f"{obj.duration_days} days"
    duration_days_display.short_description = 'Duration'

    def status_display(self, obj):
        """Displays the status with emoji"""
        return obj.status_display
    status_display.short_description = 'Status'

    def get_queryset(self, request):
        """Optimizes queryset with select_related for foreign keys"""
        return super().get_queryset(request).select_related(
            'member__person', 'ministry'
        )


admin.site.register(models.MemberMinistry, MemberMinistryAdmin)
