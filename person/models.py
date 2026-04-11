from datetime import date

from django.db import models

from app.basemodel import BaseModel


class Person(BaseModel):
    """
    People registered in the system.
    """

    class Genders(models.TextChoices):
        MALE = "M", "Masculino"
        FEMALE = "F", "Feminino"

    class MaritalStatuses(models.TextChoices):
        SINGLE = "SINGLE", "Solteiro(a)"
        MARRIED = "MARRIED", "Casado(a)"
        WIDOWED = "WIDOWED", "Viúvo(a)"
        SEPARATED = (
            "SEPARATED",
            "Separado(a)",
        )

    full_name = models.CharField(
        max_length=200, db_index=True, verbose_name="Nome Completo"
    )
    address = models.TextField(verbose_name="Endereço")
    gender = models.CharField(
        max_length=1, choices=Genders.choices, verbose_name="Gênero"
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatuses.choices,
        verbose_name="Estado Civil",
    )
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    phone = models.CharField(
        max_length=20, db_index=True, verbose_name="Telefone"
    )
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        db_table = "person"
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ["full_name"]
        indexes = [
            models.Index(fields=["full_name"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        """Calculates the person's current age"""
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - (
                (today.month, today.day)
                < (self.birth_date.month, self.birth_date.day)
            )
        )

    def get_gender_display(self):
        """Returns the gender formatted in Portuguese"""
        return dict(self.Genders.choices).get(self.gender, "")

    def get_marital_status_display(self):
        """Returns the marital status formatted in Portuguese"""
        return dict(self.MaritalStatuses.choices).get(self.marital_status, "")
