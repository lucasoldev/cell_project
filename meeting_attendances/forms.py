class MeetingAttendanceForm(forms.ModelForm):
    class Meta:
        model = models.MeetingAttendance
        fields = ['cell_meeting', 'member', 'attended', 'absence_reason', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'cell_meeting' in self.data:
            meeting_id = self.data.get('cell_meeting')
            # Filtra apenas membros que estão na célula da reunião
            self.fields['member'].queryset = Member.objects.filter(
                cell_memberships__cell__meetings__id=meeting_id,
                cell_memberships__is_active=True
            ).distinct()
