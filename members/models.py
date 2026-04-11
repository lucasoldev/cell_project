from django.db import models

from app.basemodel import BaseModel
from person.models import Person


class Member(BaseModel):
    """
    Church members linked to a person record
    """

    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,  # Se deletar Person, deleta Member também
        related_name="member_profile",
        verbose_name="Pessoa",
    )
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name="Ativo"
    )
    entry_date = models.DateField(verbose_name="Data de Entrada")
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        db_table = 'member'
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'
        ordering = ['person__full_name']
        indexes = [
            models.Index(fields=['person']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"Membro: {self.person.full_name}"

    @property
    def full_name(self):
        """Returns the member's full name"""
        return self.person.full_name

    @property
    def age(self):
        """Returns the member's age"""
        return self.person.age
