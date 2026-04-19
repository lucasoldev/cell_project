from django import forms

from . import models


class CalendarEventForm(forms.ModelForm):

    class Meta:
        model = models.CalendarEvent
        fields = ['event_date', 'event_type', 'description', 'notes']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }
