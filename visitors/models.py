from django.db import models
from app.basemodel import BaseModel
from person.models import Person
from cells.models import Cell


class Visitor(BaseModel):
    """
    Records visits of people to specific cells
    Tracks visitation history and membership conversion
    """
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='visits',
        verbose_name='Pessoa'
    )
    cell = models.ForeignKey(
        Cell,
        on_delete=models.CASCADE,
        related_name='visitors',
        verbose_name='Célula'
    )
    visit_date = models.DateField(
        db_index=True,
        verbose_name='Data da Visita'
    )
    became_member = models.BooleanField(
        default=False,
        verbose_name='Tornou-se Membro'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )

    class Meta:
        db_table = 'visitor'
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'
        ordering = ['-visit_date', 'person__full_name']
        indexes = [
            models.Index(fields=['person', 'cell']),
            models.Index(fields=['became_member']),
        ]

    def __str__(self):
        return f"{self.person.full_name} visited {self.cell.name} on {self.visit_date}"
    
    @property
    def is_converted(self):
        """Returns whether the visitor became a member"""
        return self.became_member
    
    @property
    def visit_summary(self):
        """Returns a brief summary of the visit"""
        status = "Converted" if self.became_member else "Pending"
        return f"{self.person.full_name} - {self.cell.name} ({self.visit_date}) - {status}"
