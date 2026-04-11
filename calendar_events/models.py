from django.db import models

from app.basemodel import BaseModel
from event_types.models import EventType


class CalendarEvent(BaseModel):
    """
    Calendar events for scheduling
    """

    event_date = models.DateField(
        unique=True, db_index=True, verbose_name="Data do Evento"
    )
    event_type = models.ForeignKey(
        EventType,
        on_delete=models.PROTECT,
        related_name="calendar_events",
        verbose_name="Tipo de Evento",
    )
    description = models.TextField(blank=True, verbose_name="Descrição")
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        db_table = "calendar_event"
        verbose_name = "Evento do Calendário"
        verbose_name_plural = "Eventos do Calendário"
        ordering = ["-event_date"]
        indexes = [
            models.Index(fields=["event_date"]),
            models.Index(fields=["event_type"]),
        ]

    def __str__(self):
        return f"{self.event_date} - {self.event_type.get_name_display()}"
