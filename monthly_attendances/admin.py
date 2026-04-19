from django.contrib import admin

from . import models


class MonthlyAttendanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for MonthlyAttendance model.
    Displays aggregated monthly attendance statistics for members.
    """

    list_display = (
        'member_name_display',
        'cell_name_display',
        'month_year_display',
        'attendance_summary',
        'is_faithful',
        'performance_emoji_display',
    )
    search_fields = (
        'member__person__full_name',
        'cell__name',
    )
    list_filter = (
        'is_faithful',
        'year',
        'month',
        'cell__area',
        'cell',
    )
    raw_id_fields = ('member', 'cell')
    readonly_fields = (
        'created_at',
        'updated_at',
        'attendance_percentage',
        'is_faithful',
        'member_name_display',
        'cell_name_display',
        'month_year_display',
        'performance_emoji_display',
        'summary_display',
    )

    fieldsets = (
        ('Member Information', {
            'fields': ('member', 'cell')
        }),
        ('Period', {
            'fields': ('year', 'month', 'month_year_display')
        }),
        ('Attendance Statistics', {
            'fields': ('total_meetings', 'attendances', 'attendance_percentage', 'is_faithful')
        }),
        ('Performance', {
            'fields': ('performance_emoji_display', 'summary_display'),
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

    def cell_name_display(self, obj):
        """Displays the cell name"""
        return obj.cell_name
    cell_name_display.short_description = 'Cell'
    cell_name_display.admin_order_field = 'cell__name'

    def month_year_display(self, obj):
        """Displays formatted month/year"""
        return obj.month_year_display
    month_year_display.short_description = 'Month/Year'
    month_year_display.admin_order_field = 'year'

    def attendance_summary(self, obj):
        """Displays attendance fraction and percentage"""
        if obj.total_meetings == 0:
            return 'No meetings'
        return f'{obj.attendances}/{obj.total_meetings} ({obj.attendance_percentage:.1f}%)'
    attendance_summary.short_description = 'Attendance'

    def performance_emoji_display(self, obj):
        """Displays performance emoji"""
        return obj.performance_emoji
    performance_emoji_display.short_description = 'Perf'

    def summary_display(self, obj):
        """Displays complete summary"""
        return obj.summary
    summary_display.short_description = 'Summary'

    def get_queryset(self, request):
        """Optimizes queryset with select_related for foreign keys"""
        return super().get_queryset(request).select_related(
            'member__person',
            'cell__area'
        )

    def has_add_permission(self, request):
        """
        Disable manual creation. Monthly attendance should be generated
        automatically from MeetingAttendance records.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Allow viewing but prevent manual editing of calculated fields.
        """
        return True

    def get_readonly_fields(self, request, obj=None):
        """
        Make all calculated fields readonly. Only notes can be edited.
        """
        if obj:
            return self.readonly_fields + (
                'member', 'cell', 'year', 'month', 'total_meetings', 'attendances'
            )
        return self.readonly_fields


admin.site.register(models.MonthlyAttendance, MonthlyAttendanceAdmin)
