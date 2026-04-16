from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from app.basemodel import BaseModel
from cells.models import Cell
from leadership_roles.models import LeadershipRole
from members.models import Member


class CellMember(BaseModel):
    """
    Membership records linking members to cells
    Tracks active/inactive status and optional leadership roles
    """

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="cell_memberships",
        verbose_name="Membro",
    )
    cell = models.ForeignKey(
        Cell,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Célula",
    )
    role = models.ForeignKey(
        LeadershipRole,
        on_delete=models.PROTECT,
        null=True,  # ✅ Permite nulo (membro comum sem cargo)
        blank=True,  # ✅ Permite vazio no formulário
        related_name="cell_members",
        verbose_name="Função de Liderança",
        help_text="Opcional. Preencha apenas se o membro tiver função de liderança nesta célula.",
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
        db_table = "cell_member"
        verbose_name = "Membro de Célula"
        verbose_name_plural = "Membros de Células"
        ordering = ["cell__name", "-is_active", "member__person__full_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["member", "cell"],
                condition=models.Q(is_active=True),
                name="unique_active_member_cell",
            )
        ]
        indexes = [
            models.Index(fields=["member", "cell", "is_active"]),
            models.Index(fields=["cell", "is_active"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        status = "🟢" if self.is_active else "⚪"
        role_display = f" - {self.role.title}" if self.role else ""
        return f"{status} {self.member.person.full_name} - {self.cell.name}{role_display}"

    def clean(self):
        """Validates business rules for cell membership"""
        super().clean()

        # Rule 1: Member must be active
        if not self.member.is_active:
            raise ValidationError(
                {
                    "member": "Não é possível adicionar um membro inativo à célula"
                }
            )

        # Rule 2: End date must be after start date
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

        # Rule 3: Prevent overlapping active memberships for same member in same cell
        if self.is_active and not self.pk:
            existing = CellMember.objects.filter(
                member=self.member, cell=self.cell, is_active=True
            )
            if existing.exists():
                raise ValidationError(
                    "Este membro já possui uma participação ativa nesta célula"
                )

    def save(self, *args, **kwargs):
        """Performs validation and auto-sets end_date when deactivated"""
        if not self.is_active and not self.end_date:
            self.end_date = date.today()

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def duration_days(self):
        """Returns the duration of this membership in days"""
        end = self.end_date if self.end_date else date.today()
        return (end - self.start_date).days

    @property
    def member_name(self):
        """Returns the member's full name"""
        return self.member.person.full_name

    @property
    def status_display(self):
        """Returns a user-friendly status string"""
        if self.is_active:
            return "Ativo"
        return f"Encerrado em {self.end_date}"

    @property
    def role_display(self):
        """Returns the role display or 'Membro' if no role"""
        return self.role.title if self.role else "Membro"
