from django import forms
from . import models
from person.models import Person


class MemberForm(forms.ModelForm):

    class Meta:
        model = models.Member
        fields = ['person', 'entry_date', 'is_active', 'notes']
        widgets = {
            'entry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostra apenas pessoas que AINDA NÃO são membros
        self.fields['person'].queryset = Person.objects.filter(
            member_profile__isnull=True
        ).order_by('full_name')