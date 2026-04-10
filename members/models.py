from django.db import models
from person.models import Person
from app.basemodel import BaseModel


class Member(BaseModel):
    """
    Church members linked to a person record
    """
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,  # Se deletar Person, deleta Member também
        related_name='member_profile',
        verbose_name='Pessoa'
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Ativo'
    )
    entry_date = models.DateField(
        verbose_name='Data de Entrada'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )

    class Meta:
        db_table = 'member'
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'
        ordering = ['person__full_name']

    def __str__(self):
        return f"Membro: {self.person.full_name}"