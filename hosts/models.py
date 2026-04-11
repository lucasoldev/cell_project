from django.db import models

from app.basemodel import BaseModel
from person.models import Person


class Host(BaseModel):
    """
    Host locations for cell groups/meetings
    """

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="host_locations",
        verbose_name="Anfitrião",
    )
    full_address = models.TextField(verbose_name="Endereço Completo")
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        db_table = "host"
        verbose_name = "Local de Anfitrião"
        verbose_name_plural = "Locais de Anfitriões"
        ordering = ["person__full_name"]
        indexes = [
            models.Index(fields=["person"]),
        ]

    def __str__(self):
        return (
            f"Anfitrião: {self.person.full_name} - {self.full_address[:50]}..."
        )

    @property
    def short_address(self):
        """Returns first 50 characters of address"""
        return (
            self.full_address[:50] + "..."
            if len(self.full_address) > 50
            else self.full_address
        )
