from django.db import models
from app.basemodel import BaseModel


class EventType(BaseModel):
    """
    Calendary event types
    """
    class Types(models.TextChoices):
        CELULA = 'CELULA', 'Célula'
        LIVRE = 'LIVRE', 'Livre'
        MAG = 'MAG', 'Mag'
        FERIADO = 'FERIADO', 'Feriado'

    name = models.CharField(
        max_length=10,
        choices=Types.choices,
        unique=True
    )
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()  # Mostra "Célula" em vez de "CELULA"