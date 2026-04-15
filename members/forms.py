from django import forms
from . import models


class MemberForm(forms.ModelForm):

    class Meta:
        model = models.Member
        fields = ['person', 'is_active', 'entry_date', 'notes']
        widgets = {
            'entry_date': forms.DateInput(attrs={'type': 'date'}),
        }