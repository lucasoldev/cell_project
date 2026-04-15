from django import forms
from . import models


class PersonForm(forms.ModelForm):

    class Meta:
        model = models.Person
        fields = [
            'full_name',
            'address',
            'gender',
            'marital_status',
            'birth_date',
            'phone',
            'notes',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
