from django import forms

from . import models


class CellForm(forms.ModelForm):

    class Meta:
        model = models.Cell
        fields = ['name', 'area', 'mag_branch', 'cgsbc', 'notes']
