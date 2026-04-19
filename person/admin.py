from django.contrib import admin

from . import models


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone',
        'gender',
        'marital_status',
        'birth_date',
    )
    search_fields = ('full_name', 'phone')
    list_filter = ('gender', 'marital_status')


admin.site.register(models.Person, PersonAdmin)
