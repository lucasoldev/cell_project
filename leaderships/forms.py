from django import forms

from . import models


class LeadershipForm(forms.ModelForm):

    class Meta:
        model = models.Leadership
        fields = [
            'person',
            'role',
            'area',
            'cell',
            'start_date',
            'end_date',
            'is_active',
            'notes',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
