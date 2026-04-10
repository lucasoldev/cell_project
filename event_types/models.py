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

    name = models.CharField(
        max_length=10,
        choices=Types.choices,
        unique=True,
        verbose_name='Nome'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descrição'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()
