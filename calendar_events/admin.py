from django.contrib import admin

from . import models


class CalendarEventAdmin(admin.ModelAdmin):
    """
    Admin configuration for CalendarEvent model.
    """

    list_display = (
        'event_date',
        'event_type',
        'description_preview',
        'created_at',
    )
    search_fields = (
        'description',
        'notes',
        'event_type__name',
    )
    list_filter = (
        'event_type',
        'event_date',
    )
    date_hierarchy = 'event_date'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Event Information', {
            'fields': ('event_date', 'event_type')
        }),
        ('Details', {
            'fields': ('description', 'notes')
        }),
        ('System Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def description_preview(self, obj):
        """Displays a preview of the description"""
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '—'
    description_preview.short_description = 'Description'

    def get_queryset(self, request):
        """Optimizes queryset with select_related for foreign keys"""
        return super().get_queryset(request).select_related('event_type')


admin.site.register(models.CalendarEvent, CalendarEventAdmin)
