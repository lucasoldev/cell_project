from django.db import models
from django.core.exceptions import ValidationError
from app.basemodel import BaseModel
from cell_meetings.models import CellMeeting
from members.models import Member


class MeetingAttendance(BaseModel):
    """
    Individual attendance records for cell meetings
    Tracks presence/absence and reasons for each member per meeting
    """
    cell_meeting = models.ForeignKey(
        CellMeeting,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='Reunião'
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='Membro'
    )
    attended = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Presente'
    )
    absence_reason = models.TextField(
        blank=True,
        verbose_name='Motivo da Ausência'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )

    class Meta:
        db_table = 'meeting_attendance'
        verbose_name = 'Presença em Reunião'
        verbose_name_plural = 'Presenças em Reuniões'
        ordering = ['-cell_meeting__meeting_date', 'member__person__full_name']
        constraints = [
            models.UniqueConstraint(
                fields=['cell_meeting', 'member'],
                name='unique_attendance_per_meeting'
            )
        ]
        indexes = [
            models.Index(fields=['cell_meeting', 'attended']),
            models.Index(fields=['member', 'attended']),
            models.Index(fields=['attended']),
        ]

    def __str__(self):
        status = "✅" if self.attended else "❌"
        return f"{status} {self.member.person.full_name} - {self.cell_meeting.meeting_date.strftime('%d/%m/%Y')}"

    def clean(self):
        """Validates business rules for meeting attendance"""
        super().clean()
        
        # Rule 1: Member must be active
        if self.member_id and not self.member.is_active:
            raise ValidationError({
                'member': 'Não é possível registrar presença para um membro inativo'
            })
        
        # Rule 2: Absence reason required when not attended
        if not self.attended and not self.absence_reason:
            raise ValidationError({
                'absence_reason': 'É necessário informar o motivo da ausência'
            })
        
        # Rule 3: Absence reason should be empty when attended
        if self.attended and self.absence_reason:
            raise ValidationError({
                'absence_reason': 'Não deve haver motivo de ausência quando o membro está presente'
            })
        
        # Rule 4: Member should belong to the meeting's cell (optional validation)
        if self.member_id and self.cell_meeting_id:
            # Check if member is active in this cell
            from cell_member.models import CellMember
            is_cell_member = CellMember.objects.filter(
                member=self.member,
                cell=self.cell_meeting.cell,
                is_active=True
            ).exists()
            
            if not is_cell_member:
                raise ValidationError({
                    'member': 'Este membro não está ativo nesta célula'
                })
        
        # Rule 5: Meeting must have taken place
        if self.cell_meeting_id and not self.cell_meeting.took_place:
            raise ValidationError({
                'cell_meeting': 'Não é possível registrar presença em uma reunião cancelada'
            })

    def save(self, *args, **kwargs):
        """Performs validation and updates meeting total_attendees"""
        is_new = self.pk is None
        old_attended = None
        
        if not is_new:
            old_instance = MeetingAttendance.objects.get(pk=self.pk)
            old_attended = old_instance.attended
        
        self.full_clean()
        super().save(*args, **kwargs)
        
        # Update meeting total_attendees count
        self.update_meeting_attendees_count(is_new, old_attended)
    
    def update_meeting_attendees_count(self, is_new, old_attended):
        """Updates the total_attendees count on the related meeting"""
        meeting = self.cell_meeting
        
        if is_new:
            if self.attended:
                meeting.total_attendees += 1
        else:
            if old_attended and not self.attended:
                meeting.total_attendees -= 1
            elif not old_attended and self.attended:
                meeting.total_attendees += 1
        
        meeting.save(update_fields=['total_attendees'])
    
    def delete(self, *args, **kwargs):
        """Decrement meeting total_attendees when attendance is deleted"""
        if self.attended:
            self.cell_meeting.total_attendees -= 1
            self.cell_meeting.save(update_fields=['total_attendees'])
        super().delete(*args, **kwargs)
    
    @property
    def status_display(self):
        """Returns a user-friendly status string"""
        if self.attended:
            return "✅ Presente"
        return f"❌ Ausente - {self.absence_reason[:50]}..."
    
    @property
    def member_name(self):
        """Returns the member's full name"""
        return self.member.person.full_name
    
    @property
    def meeting_date_display(self):
        """Returns formatted meeting date"""
        return self.cell_meeting.meeting_date.strftime('%d/%m/%Y')
    
    @property
    def cell_name(self):
        """Returns the cell name"""
        return self.cell_meeting.cell.name