from django import forms

from . import models


class MinistryForm(forms.ModelForm):

    class Meta:
        model = models.Ministry
        fields = ['name', 'description', 'notes']
