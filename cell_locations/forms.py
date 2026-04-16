from django import forms
from . import models


class CellLocationForm(forms.ModelForm):

    class Meta:
        model = models.CellLocation
        fields = ['cell', 'host', 'address', 'is_active', 'notes']
