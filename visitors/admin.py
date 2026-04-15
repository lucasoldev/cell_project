from django.contrib import admin
from . import models


class VisitorAdmin(admin.ModelAdmin):
    list_display = (
        'person',
        'cell',
        'visit_date',
        'became_member',
    )
    search_fields = ('person__full_name', 'cell__name')
    list_filter = ('became_member', 'visit_date', 'cell')
    raw_id_fields = ('person', 'cell')
    date_hierarchy = 'visit_date'


admin.site.register(models.Visitor, VisitorAdmin)
