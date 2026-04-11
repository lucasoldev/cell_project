from django.db import models

from app.basemodel import BaseModel
from cells.models import Cell
from hosts.models import Host


class CellLocation(BaseModel):
    """
    Physical locations where cell meetings take place
    Tracks address history and active status for each cell
    """

    cell = models.ForeignKey(
        Cell,
        on_delete=models.CASCADE,
        related_name="locations",
        verbose_name="Célula",
    )
    host = models.ForeignKey(
        Host,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cell_locations",
        verbose_name="Anfitrião",
    )
    address = models.TextField(verbose_name="Endereço")
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name="Ativo"
    )
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        db_table = "cell_location"
        verbose_name = "Local de Célula"
        verbose_name_plural = "Locais de Células"
        ordering = ["-is_active", "cell__name"]
        indexes = [
            models.Index(fields=["cell", "is_active"]),
            models.Index(fields=["host"]),
        ]

    def __str__(self):
        return f"{self.cell.name} @ {self.address[:50]}"

    @property
    def short_address(self):
        """Returns first 50 characters of the address for display purposes"""
        return (
            self.address[:50] + "..."
            if len(self.address) > 50
            else self.address
        )

    @property
    def host_name(self):
        """Returns the host's full name if available"""
        if self.host:
            return self.host.person.full_name
        return "No host assigned"
