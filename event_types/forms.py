from django import forms
from . import models


class EventTypeForm(forms.ModelForm):

    class Meta:
        model = models.EventType
        fields = ['name', 'description']
