from django import forms
from . import models


class AreaForm(forms.ModelForm):
    """
    Form for Area model. Only used for validation, not for creation/editing.
    """

    class Meta:
        model = models.Area
        fields = ['color', 'is_mag', 'notes']
