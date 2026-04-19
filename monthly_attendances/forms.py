from django import forms

from . import models


class MonthlyAttendanceForm(forms.ModelForm):

    class Meta:
        model = models.MonthlyAttendance
        fields = [
            'member',
            'cell',
            'year',
            'month',
            'total_meetings',
            'attendances',
            'notes',
        ]
        widgets = {
            'year': forms.NumberInput(attrs={'min': 2020, 'max': 2100}),
            'month': forms.Select(choices=models.MonthlyAttendance.Month.choices),
        }
