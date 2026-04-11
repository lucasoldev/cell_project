from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from app.basemodel import BaseModel
from areas.models import Area
from cells.models import Cell
from leadership_roles.models import LeadershipRole
from person.models import Person


class Leadership(BaseModel):
    """
    Leadership positions in the church hierarchy
    Tracks assignments of people to leadership roles with areas/cells
    """

    # Leadership Role Hierarchy (for reference):
    # 1: Pastor (highest)
    # 2: Supervisor de Área
    # 3: Supervisor de Célula
    # 4: Facilitador
    # 5: Auxiliar (lowest)

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="leadership_positions",
        verbose_name="Pessoa",
    )
    role = models.ForeignKey(
        LeadershipRole,
        on_delete=models.PROTECT,
        related_name="leaders",
        verbose_name="Cargo",
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="leaders",
        verbose_name="Área",
    )
    cell = models.ForeignKey(
        Cell,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="leaders",
        verbose_name="Célula",
    )
    start_date = models.DateField(verbose_name="Data de Início")
    end_date = models.DateField(
        null=True, blank=True, verbose_name="Data de Término"
    )
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name="Ativo"
    )
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        db_table = "leadership"
        verbose_name = "Liderança"
        verbose_name_plural = "Lideranças"
        ordering = ["-is_active", "role__hierarchy_level", "start_date"]
        indexes = [
            models.Index(fields=["person", "is_active"]),
            models.Index(fields=["role", "is_active"]),
            models.Index(fields=["area", "is_active"]),
            models.Index(fields=["cell", "is_active"]),
        ]

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.person.full_name} - {self.role.title} ({status})"

    def clean(self):
        """Validates business rules for leadership assignments"""
        super().clean()

        # Skip validation if role is not set yet
        if not self.role_id:
            return

        # Fetch role from database if needed
        if hasattr(self, "role") and isinstance(self.role, LeadershipRole):
            role = self.role
        else:
            role = LeadershipRole.objects.get(pk=self.role_id)

        # Rule 1: Area Supervisor (hierarchy_level=2) must have an area
        if role.hierarchy_level == 2 and not self.area:
            raise ValidationError(
                {"area": "Supervisor de Área deve estar vinculado a uma área"}
            )

        # Rule 2: Cell leaders (hierarchy_level 4 or 5) must have a cell
        if role.hierarchy_level in [4, 5] and not self.cell:
            raise ValidationError(
                {
                    "cell": "Facilitador e Auxiliar devem estar vinculados a uma célula"
                }
            )

        # Rule 3: Cell Supervisor (hierarchy_level=3) - optional validation
        if role.hierarchy_level == 3:
            if not self.cell and not self.area:
                raise ValidationError(
                    "Supervisor de Célula deve estar vinculado a uma célula ou área"
                )

        # Rule 4: Pastor (hierarchy_level=1) doesn't need area or cell
        # (No validation needed)

        # Rule 5: End date must be after start date
        if (
            self.end_date
            and self.start_date
            and self.end_date < self.start_date
        ):
            raise ValidationError(
                {
                    "end_date": "Data de término não pode ser anterior à data de início"
                }
            )

        # Rule 6: Prevent overlapping active leadership for same person/role?
        if self.is_active and not self.pk:  # Only for new records
            existing = Leadership.objects.filter(
                person_id=self.person_id, role_id=self.role_id, is_active=True
            )
            if self.area_id:
                existing = existing.filter(area_id=self.area_id)
            if self.cell_id:
                existing = existing.filter(cell_id=self.cell_id)

            if existing.exists():
                raise ValidationError(
                    "Esta pessoa já possui uma liderança ativa neste cargo/área/célula"
                )

    def save(self, *args, **kwargs):
        """Performs validation and auto-sets end_date when deactivated"""
        if not self.is_active and not self.end_date:
            self.end_date = date.today()

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def duration_days(self):
        """Returns the duration of this leadership assignment in days"""
        end = self.end_date if self.end_date else date.today()
        return (end - self.start_date).days

    @property
    def status_display(self):
        """Returns a user-friendly status string"""
        if self.is_active:
            return "🟢 Ativo"
        return f"⚪ Encerrado em {self.end_date}"
