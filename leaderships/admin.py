from django.contrib import admin

from . import models


class LeadershipAdmin(admin.ModelAdmin):
    """
    Admin configuration for Leadership model.
    Tracks assignments of people to leadership roles with areas/cells.
    """

    list_display = (
        'person',
        'role',
        'assignment_display',
        'is_active',
        'start_date',
        'end_date',
    )
    search_fields = (
        'person__full_name',
        'role__title',
        'area__color',
        'cell__name',
    )
    list_filter = (
        'is_active',
        'role',
        'area',
        'start_date',
    )
    raw_id_fields = ('person', 'role', 'area', 'cell')
    date_hierarchy = 'start_date'
    readonly_fields = (
        'created_at',
        'updated_at',
        'duration_days_display',
        'status_display',
    )

    fieldsets = (
        ('Basic Information', {
            'fields': ('person', 'role', 'is_active', 'status_display')
        }),
        ('Assignment', {
            'fields': ('area', 'cell'),
            'description': 'Fill according to role: Area Supervisor requires Area; Facilitator/Auxiliary requires Cell.'
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

    def assignment_display(self, obj):
        """Displays the area or cell based on assignment"""
        if obj.area:
            return f"Área: {obj.area.get_color_display()}"
        elif obj.cell:
            return f"Célula: {obj.cell.name}"
        return "—"
    assignment_display.short_description = 'Assignment'

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
            'person', 'role', 'area', 'cell'
        )


admin.site.register(models.Leadership, LeadershipAdmin)
