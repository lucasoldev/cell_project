from django import forms
from . import models


class CellMemberForm(forms.ModelForm):

    class Meta:
        model = models.CellMember
        fields = [
            'member',
            'cell',
            'role',
            'start_date',
            'end_date',
            'is_active',
            'notes',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
