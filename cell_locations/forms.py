from django import forms
from . import models


class CellLocationForm(forms.ModelForm):
    class Meta:
        model = models.CellLocation
        fields = ['cell', 'host', 'address', 'is_active', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostra apenas locais ATIVOS (para edição, pode ser diferente)
        if not self.instance.pk:  # Apenas na criação
            self.fields['host'].queryset = Host.objects.all()
