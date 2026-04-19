from django import forms

from . import models


class VisitorForm(forms.ModelForm):

    class Meta:
        model = models.Visitor
        fields = ['person', 'cell', 'visit_date', 'became_member', 'notes']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
        }
