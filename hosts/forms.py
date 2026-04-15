from django import forms
from . import models


class HostForm(forms.ModelForm):

    class Meta:
        model = models.Host
        fields = ['person', 'full_address', 'notes']
