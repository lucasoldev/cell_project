from django.db import models

from app.basemodel import BaseModel


class Area(BaseModel):
    """
    Areas of church cell supervision (Red, Yellow, Blue, Green, White)
    """

    class AreaColor(models.TextChoices):
        VERMELHA = "RED", "Vermelha"
        AMARELA = "YELLOW", "Amarela"
        AZUL = "BLUE", "Azul"
        VERDE = "GREEN", "Verde"
        BRANCA = "WHITE", "Branca"

    color = models.CharField(
        max_length=20,
        choices=AreaColor.choices,
        unique=True,  # Garante que não tenha áreas duplicadas
    )
    is_mag = models.BooleanField(
        default=False, help_text="Marque se for a área MAG (Área Vermelha)"
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'area'
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['color']
        constraints = [
            models.CheckConstraint(
                check=models.Q(is_mag=True, color='RED') | models.Q(is_mag=False),
                name='mag_area_must_be_red'
            )
        ]

    def __str__(self):
        return self.get_color_display()

    def save(self, *args, **kwargs):
        """Ensures MAG area is always red"""
        if self.is_mag:
            self.color = self.AreaColor.VERMELHA
        super().save(*args, **kwargs)
