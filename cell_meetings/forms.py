from django import forms
from . import models
from cell_locations.models import CellLocation
from calendar_events.models import CalendarEvent
from datetime import date


class CellMeetingForm(forms.ModelForm):

    class Meta:
        model = models.CellMeeting
        fields = [
            'cell',
            'cell_location',
            'calendar_event',
            'meeting_date',
            'took_place',
            'total_attendees',
            'notes',
        ]
        widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas locais ativos
        self.fields['cell_location'].queryset = CellLocation.objects.filter(is_active=True)
        # Filtra apenas eventos futuros ou de hoje (opcional no form)
        self.fields['calendar_event'].required = False
