from django import forms

from . import models


class MemberMinistryForm(forms.ModelForm):

    class Meta:
        model = models.MemberMinistry
        fields = [
            'member',
            'ministry',
            'start_date',
            'end_date',
            'is_active',
            'notes',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas membros ativos
        from members.models import Member
        self.fields['member'].queryset = Member.objects.filter(
            is_active=True
        ).select_related('person')
