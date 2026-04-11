from django.db import models

from app.basemodel import BaseModel


class LeadershipRole(BaseModel):
    """
    Leadership roles in the church hierarchy
    """

    class Roles(models.TextChoices):
        PASTOR = "PASTOR", "Pastor"
        SUPERVISOR_AREA = "SUPERVISOR_AREA", "Supervisor de Área"
        SUPERVISOR_CELULA = "SUPERVISOR_CELULA", "Supervisor de Célula"
        FACILITADOR = "FACILITADOR", "Facilitador"
        AUXILIAR = "AUXILIAR", "Auxiliar"

    title = models.CharField(max_length=20, choices=Roles.choices, unique=True)
    description = models.TextField(null=True, blank=True)
    hierarchy_level = models.IntegerField(
        editable=False, help_text="Definido automaticamente baseado no cargo"
    )

    class Meta:
        db_table = 'leadership_role'
        verbose_name = 'Cargo de Liderança'
        verbose_name_plural = 'Cargos de Liderança'
        ordering = ['hierarchy_level']

    def __str__(self):
        return self.get_title_display()

    def save(self, *args, **kwargs):
        """Auto-sets hierarchy level based on role"""
        hierarchy_map = {
            self.Roles.PASTOR: 1,
            self.Roles.SUPERVISOR_AREA: 2,
            self.Roles.SUPERVISOR_CELULA: 3,
            self.Roles.FACILITADOR: 4,
            self.Roles.AUXILIAR: 5,
        }
        self.hierarchy_level = hierarchy_map.get(self.title, 99)
        super().save(*args, **kwargs)
