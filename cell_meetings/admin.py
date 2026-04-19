from django.contrib import admin

from . import models


class CellMeetingAdmin(admin.ModelAdmin):
    """
    Admin configuration for CellMeeting model.
    """

    list_display = (
        'cell',
        'meeting_date',
        'day_of_week_display',
        'took_place',
        'total_attendees',
        'host_name_display',
    )
    search_fields = (
        'cell__name',
        'cell_location__address',
        'notes',
    )
    list_filter = (
        'took_place',
        'cell__area',
        'cell',
        'meeting_date',
    )
    date_hierarchy = 'meeting_date'
    raw_id_fields = ('cell', 'cell_location', 'calendar_event')
    readonly_fields = (
        'created_at',
        'updated_at',
        'day_of_week_display',
        'host_name_display',
        'location_address_display',
        'status_display',
        'meeting_summary_display',
    )

    fieldsets = (
        ('Meeting Information', {
            'fields': ('cell', 'cell_location', 'meeting_date', 'took_place')
        }),
        ('Attendance', {
            'fields': ('total_attendees',)
        }),
        ('Calendar Event', {
            'fields': ('calendar_event',),
            'description': 'Optional. Link to a calendar event.'
        }),
        ('Additional Information', {
            'fields': ('host_name_display', 'location_address_display', 'day_of_week_display'),
        }),
        ('Status Summary', {
            'fields': ('status_display', 'meeting_summary_display'),
        }),
        ('Notes', {
            'fields': ('notes',),
        }),
        ('System Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def day_of_week_display(self, obj):
        """Displays the day of the week in Portuguese"""
        return obj.day_of_week
    day_of_week_display.short_description = 'Day of Week'

    def host_name_display(self, obj):
        """Displays the host's full name"""
        return obj.host_name
    host_name_display.short_description = 'Host'

    def location_address_display(self, obj):
        """Displays the meeting location address"""
        return obj.location_address
    location_address_display.short_description = 'Address'

    def status_display(self, obj):
        """Displays the meeting status with emoji"""
        return obj.status_display
    status_display.short_description = 'Status'

    def meeting_summary_display(self, obj):
        """Displays a complete meeting summary"""
        return obj.meeting_summary
    meeting_summary_display.short_description = 'Summary'

    def get_queryset(self, request):
        """Optimizes queryset with select_related for foreign keys"""
        return super().get_queryset(request).select_related(
            'cell__area',
            'cell_location__host__person',
            'calendar_event__event_type'
        )


admin.site.register(models.CellMeeting, CellMeetingAdmin)
