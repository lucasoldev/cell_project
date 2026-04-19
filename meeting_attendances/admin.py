from django.contrib import admin

from . import models


class MeetingAttendanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for MeetingAttendance model.
    Tracks individual attendance records for cell meetings.
    """

    list_display = (
        'member_name_display',
        'cell_name_display',
        'meeting_date_display',
        'attended',
        'absence_reason_preview',
    )
    search_fields = (
        'member__person__full_name',
        'cell_meeting__cell__name',
        'absence_reason',
    )
    list_filter = (
        'attended',
        'cell_meeting__cell__area',
        'cell_meeting__cell',
        'cell_meeting__meeting_date',
    )
    date_hierarchy = 'cell_meeting__meeting_date'
    raw_id_fields = ('cell_meeting', 'member')
    readonly_fields = (
        'created_at',
        'updated_at',
        'member_name_display',
        'cell_name_display',
        'meeting_date_display',
        'status_display',
    )

    fieldsets = (
        ('Attendance Information', {
            'fields': ('cell_meeting', 'member', 'attended')
        }),
        ('Absence Details', {
            'fields': ('absence_reason',),
            'description': 'Required only when member is absent.'
        }),
        ('Additional Information', {
            'fields': ('member_name_display', 'cell_name_display', 'meeting_date_display', 'status_display'),
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
        try:
            return obj.member_name
        except Exception:
            return "—"
    member_name_display.short_description = 'Member'

    def cell_name_display(self, obj):
        """Displays the cell name"""
        try:
            return obj.cell_name
        except Exception:
            return "—"
    cell_name_display.short_description = 'Cell'

    def meeting_date_display(self, obj):
        """Displays formatted meeting date"""
        try:
            return obj.meeting_date_display
        except Exception:
            return "—"
    meeting_date_display.short_description = 'Meeting Date'

    def absence_reason_preview(self, obj):
        """Displays a preview of the absence reason"""
        if obj.absence_reason:
            return obj.absence_reason[:30] + '...' if len(obj.absence_reason) > 30 else obj.absence_reason
        return '—'
    absence_reason_preview.short_description = 'Absence Reason'

    def status_display(self, obj):
        """Displays the status with emoji"""
        try:
            return obj.status_display
        except Exception:
            return "—"
    status_display.short_description = 'Status'

    def get_queryset(self, request):
        """Optimizes queryset with select_related for foreign keys"""
        return super().get_queryset(request).select_related(
            'cell_meeting__cell__area',
            'member__person'
        )


admin.site.register(models.MeetingAttendance, MeetingAttendanceAdmin)
