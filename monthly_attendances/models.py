from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from app.basemodel import BaseModel
from cells.models import Cell
from meeting_attendances.models import MeetingAttendance
from members.models import Member


class MonthlyAttendance(BaseModel):
    """
    Aggregated monthly attendance statistics for members per cell
    Denormalized table for performance optimization in reports and dashboards
    """

    class Month(models.IntegerChoices):
        JANUARY = 1, "Janeiro"
        FEBRUARY = 2, "Fevereiro"
        MARCH = 3, "Março"
        APRIL = 4, "Abril"
        MAY = 5, "Maio"
        JUNE = 6, "Junho"
        JULY = 7, "Julho"
        AUGUST = 8, "Agosto"
        SEPTEMBER = 9, "Setembro"
        OCTOBER = 10, "Outubro"
        NOVEMBER = 11, "Novembro"
        DECEMBER = 12, "Dezembro"

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="monthly_attendances",
        verbose_name="Membro",
    )
    cell = models.ForeignKey(
        Cell,
        on_delete=models.CASCADE,
        related_name="monthly_attendances",
        verbose_name="Célula",
    )
    year = models.IntegerField(
        validators=[MinValueValidator(2020), MaxValueValidator(2100)],
        verbose_name="Ano",
    )
    month = models.IntegerField(
        choices=Month.choices,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Mês",
    )
    total_meetings = models.PositiveIntegerField(
        default=0, verbose_name="Total de Reuniões"
    )
    attendances = models.PositiveIntegerField(
        default=0, verbose_name="Presenças"
    )
    attendance_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Percentual de Presença",
    )
    is_faithful = models.BooleanField(
        default=False, db_index=True, verbose_name="Fiel"
    )
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        db_table = "monthly_attendance"
        verbose_name = "Frequência Mensal"
        verbose_name_plural = "Frequências Mensais"
        ordering = [
            "-year",
            "-month",
            "-attendance_percentage",
            "member__person__full_name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["member", "cell", "year", "month"],
                name="unique_monthly_attendance",
            ),
            models.CheckConstraint(
                check=models.Q(attendances__lte=models.F("total_meetings")),
                name="attendances_cannot_exceed_total_meetings",
            ),
            models.CheckConstraint(
                check=models.Q(
                    attendance_percentage__gte=0.00,
                    attendance_percentage__lte=100.00,
                ),
                name="attendance_percentage_range",
            ),
        ]
        indexes = [
            models.Index(fields=["member", "year", "month"]),
            models.Index(fields=["cell", "year", "month"]),
            models.Index(fields=["year", "month"]),
            models.Index(fields=["is_faithful", "year", "month"]),
            models.Index(fields=["attendance_percentage"]),
        ]

    def __str__(self):
        return f"{self.member.person.full_name} - {self.get_month_display()}/{self.year}: {self.attendance_percentage:.1f}%"

    def clean(self):
        """Validates business rules for monthly attendance"""
        super().clean()

        # Rule 1: Member must be active
        if self.member_id and not self.member.is_active:
            raise ValidationError(
                {
                    "member": "Não é possível registrar frequência para um membro inativo"
                }
            )

        # Rule 2: Attendances cannot exceed total meetings
        if self.attendances > self.total_meetings:
            raise ValidationError(
                {
                    "attendances": "Número de presenças não pode exceder o total de reuniões"
                }
            )

        # Rule 3: Percentage consistency
        if self.total_meetings > 0:
            calculated = (self.attendances / self.total_meetings) * 100
            if abs(float(self.attendance_percentage) - calculated) > 0.01:
                raise ValidationError(
                    {
                        "attendance_percentage": f"Percentual inconsistente. Deveria ser {calculated:.2f}%"
                    }
                )

        # Rule 4: Faithful consistency
        should_be_faithful = (
            self.attendance_percentage >= 75.00
            if self.total_meetings > 0
            else False
        )
        if self.is_faithful != should_be_faithful:
            raise ValidationError(
                {
                    "is_faithful": f"Status de fidelidade inconsistente. Deveria ser {should_be_faithful}"
                }
            )

        # Rule 5: Cannot have attendance without meetings
        if self.total_meetings == 0 and self.attendances > 0:
            raise ValidationError(
                {"total_meetings": "Não pode haver presenças sem reuniões"}
            )

    def save(self, *args, **kwargs):
        """Calculates derived fields before saving"""
        self.calculate_derived_fields()
        self.full_clean()
        super().save(*args, **kwargs)

    def calculate_derived_fields(self):
        """Calculates attendance percentage and faithful status"""
        if self.total_meetings > 0:
            self.attendance_percentage = (
                self.attendances / self.total_meetings
            ) * 100
            self.is_faithful = self.attendance_percentage >= 75.00
        else:
            self.attendance_percentage = 0.00
            self.is_faithful = False

    @classmethod
    def calculate_for_member_cell_month(cls, member, cell, year, month):
        """
        Calculates monthly attendance from MeetingAttendance records
        Returns a MonthlyAttendance instance (not saved)
        """

        # Get all meetings for this cell in the given month/year
        attendances = MeetingAttendance.objects.filter(
            member=member,
            cell_meeting__cell=cell,
            cell_meeting__meeting_date__year=year,
            cell_meeting__meeting_date__month=month,
            cell_meeting__took_place=True,
        )

        total_meetings = attendances.count()
        present_count = attendances.filter(attended=True).count()

        return cls(
            member=member,
            cell=cell,
            year=year,
            month=month,
            total_meetings=total_meetings,
            attendances=present_count,
        )

    @classmethod
    def update_or_create_from_meetings(cls, member, cell, year, month):
        """
        Updates or creates monthly attendance based on actual meeting records
        """
        instance = cls.calculate_for_member_cell_month(
            member, cell, year, month
        )
        instance.calculate_derived_fields()

        return cls.objects.update_or_create(
            member=member,
            cell=cell,
            year=year,
            month=month,
            defaults={
                "total_meetings": instance.total_meetings,
                "attendances": instance.attendances,
                "attendance_percentage": instance.attendance_percentage,
                "is_faithful": instance.is_faithful,
            },
        )

    @property
    def month_year_display(self):
        """Returns formatted month/year in Portuguese"""
        return f"{self.get_month_display()}/{self.year}"

    @property
    def member_name(self):
        """Returns the member's full name"""
        return self.member.person.full_name

    @property
    def cell_name(self):
        """Returns the cell name"""
        return self.cell.name

    @property
    def performance_emoji(self):
        """Returns an emoji based on attendance performance"""
        if self.total_meetings == 0:
            return "⚪"
        if self.attendance_percentage >= 90:
            return "🟢"
        elif self.attendance_percentage >= 75:
            return "🟡"
        elif self.attendance_percentage >= 50:
            return "🟠"
        else:
            return "🔴"

    @property
    def summary(self):
        """Returns a complete summary of monthly attendance"""
        if self.total_meetings == 0:
            return (
                f"{self.member_name} - {self.month_year_display}: Sem reuniões"
            )

        return (
            f"{self.performance_emoji} {self.member_name} - {self.month_year_display}: "
            f"{self.attendances}/{self.total_meetings} ({self.attendance_percentage:.1f}%) - "
            f'{"Fiel" if self.is_faithful else "Infrequente"}'
        )
