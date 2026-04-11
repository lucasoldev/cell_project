from django.core.exceptions import ValidationError
from django.db import models

from app.basemodel import BaseModel
from areas.models import Area
from mag_branches.models import MagBranch


class Cell(BaseModel):
    """
    Church cells organized by area
    """

    name = models.CharField(max_length=100, db_index=True, verbose_name="Nome")
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="cells",
        verbose_name="Área",
    )
    mag_branch = models.ForeignKey(
        MagBranch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="cells",
        verbose_name="Ramificação MAG",
    )
    cgsbc = models.CharField(
        max_length=100,
        blank=True,
        help_text="Church name for non-MAG cells",
        verbose_name="CGSBC",
    )
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        db_table = "cell"
        verbose_name = "Célula"
        verbose_name_plural = "Células"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.area.get_color_display()}"

    def clean(self):
        """Validates business rules for cells"""
        super().clean()

        if not self.area_id:
            return

        # Fetch area from database if needed
        if hasattr(self, "area") and isinstance(self.area, Area):
            area = self.area
        else:
            area = Area.objects.get(pk=self.area_id)

        # Business rules validation
        if area.is_mag and not self.mag_branch:
            raise ValidationError(
                {"mag_branch": "MAG cells must have a branch selected"}
            )

        if not area.is_mag and self.mag_branch:
            raise ValidationError(
                {"mag_branch": "Non-MAG cells cannot have a branch"}
            )

    def save(self, *args, **kwargs):
        """Performs full validation before saving"""
        self.full_clean()
        super().save(*args, **kwargs)
