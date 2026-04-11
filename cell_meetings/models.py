from django.db import models
from django.core.exceptions import ValidationError
from app.basemodel import BaseModel
from cells.models import Cell
from cell_locations.models import CellLocation
from calendar_events.models import CalendarEvent


class CellMeeting(BaseModel):
    """
    Records cell meetings including location, attendance, and status
    Tracks whether meetings took place and total attendee count
    """
    cell = models.ForeignKey(
        Cell,
        on_delete=models.CASCADE,
        related_name='meetings',
        verbose_name='Célula'
    )
    cell_location = models.ForeignKey(
        CellLocation,
        on_delete=models.PROTECT,
        related_name='meetings',
        verbose_name='Local da Célula'
    )
    calendar_event = models.ForeignKey(
        CalendarEvent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cell_meetings',
        verbose_name='Evento no Calendário'
    )
    meeting_date = models.DateField(
        db_index=True,
        verbose_name='Data da Reunião'
    )
    took_place = models.BooleanField(
        default=True,
        verbose_name='Realizada'
    )
    total_attendees = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de Presentes'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )

    class Meta:
        db_table = 'cell_meeting'
        verbose_name = 'Reunião de Célula'
        verbose_name_plural = 'Reuniões de Células'
        ordering = ['-meeting_date', 'cell__name']
        constraints = [
            models.UniqueConstraint(
                fields=['cell', 'meeting_date'],
                name='unique_cell_meeting_per_day'
            )
        ]
        indexes = [
            models.Index(fields=['cell', 'meeting_date']),
            models.Index(fields=['meeting_date']),
            models.Index(fields=['took_place']),
            models.Index(fields=['cell', 'took_place']),
        ]

    def __str__(self):
        status = "✓" if self.took_place else "✗"
        return f"{status} {self.cell.name} - {self.meeting_date.strftime('%d/%m/%Y')}"

    def clean(self):
        """Validates business rules for cell meetings"""
        super().clean()
        
        # Rule 1: Meeting date cannot be in the future for meetings that took place
        from datetime import date
        if self.took_place and self.meeting_date > date.today():
            raise ValidationError({
                'meeting_date': 'Não é possível registrar uma reunião realizada em data futura'
            })
        
        # Rule 2: Cell location must be active
        if self.cell_location_id and not self.cell_location.is_active:
            raise ValidationError({
                'cell_location': 'Não é possível usar um local de célula inativo'
            })
        
        # Rule 3: Cell location must belong to the selected cell
        if self.cell_id and self.cell_location_id:
            if self.cell_location.cell_id != self.cell_id:
                raise ValidationError({
                    'cell_location': 'O local selecionado não pertence a esta célula'
                })
        
        # Rule 4: Calendar event date must match meeting date (if provided)
        if self.calendar_event and self.calendar_event.event_date != self.meeting_date:
            raise ValidationError({
                'calendar_event': 'A data do evento no calendário deve coincidir com a data da reunião'
            })

    def save(self, *args, **kwargs):
        """Performs validation before saving"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def status_display(self):
        """Returns a user-friendly status string"""
        if self.took_place:
            return "✅ Realizada"
        return "❌ Cancelada"
    
    @property
    def meeting_summary(self):
        """Returns a brief summary of the meeting"""
        status = "Realizada" if self.took_place else "Cancelada"
        return f"{self.cell.name} - {self.meeting_date.strftime('%d/%m/%Y')} - {status} - {self.total_attendees} presentes"
    
    @property
    def location_address(self):
        """Returns the meeting location address"""
        return self.cell_location.address
    
    @property
    def host_name(self):
        """Returns the host name for this meeting"""
        if self.cell_location.host:
            return self.cell_location.host.person.full_name
        return "Sem anfitrião definido"
    
    @property
    def day_of_week(self):
        """Returns the day of the week in Portuguese"""
        days = {
            0: 'Segunda-feira',
            1: 'Terça-feira',
            2: 'Quarta-feira',
            3: 'Quinta-feira',
            4: 'Sexta-feira',
            5: 'Sábado',
            6: 'Domingo'
        }
        return days[self.meeting_date.weekday()]