from django import forms
from datetime import date
from . import models
from members.models import Member


class MeetingAttendanceForm(forms.ModelForm):

    class Meta:
        model = models.MeetingAttendance
        fields = [
            'cell_meeting',
            'member',
            'attended',
            'absence_reason',
            'notes',
        ]
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'absence_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Informe o motivo da ausência...'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observações adicionais (opcional)...'
            }),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtra apenas reuniões válidas
        self.fields['cell_meeting'].queryset = models.CellMeeting.objects.filter(
            meeting_date__lte=date.today(),
            took_place=True
        ).select_related('cell').order_by('-meeting_date')
        self.fields['cell_meeting'].widget.attrs.update({'class': 'form-select'})
        
        # Inicialmente, mostra apenas membros ativos (será filtrado após selecionar reunião via POST)
        self.fields['member'].queryset = Member.objects.filter(
            is_active=True
        ).select_related('person')
