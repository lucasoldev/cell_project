from django.db import models
from django.core.exceptions import ValidationError
from app.basemodel import BaseModel
from members.models import Member
from ministries.models import Ministry


class MemberMinistry(BaseModel):
    """
    Records member participation in church ministries
    Tracks active/inactive status and participation duration
    """
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='ministries',
        verbose_name='Membro'
    )
    ministry = models.ForeignKey(
        Ministry,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='Ministério'
    )
    start_date = models.DateField(
        verbose_name='Data de Início'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Término'
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Ativo'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )

    class Meta:
        db_table = 'member_ministry'
        verbose_name = 'Membro de Ministério'
        verbose_name_plural = 'Membros de Ministérios'
        ordering = ['-is_active', 'member__person__full_name', 'ministry__name']
        constraints = [
            models.UniqueConstraint(
                fields=['member', 'ministry'],
                condition=models.Q(is_active=True),
                name='unique_active_member_ministry'
            )
        ]
        indexes = [
            models.Index(fields=['member', 'is_active']),
            models.Index(fields=['ministry', 'is_active']),
            models.Index(fields=['start_date']),
        ]

    def __str__(self):
        status = "🟢" if self.is_active else "⚪"
        return f"{status} {self.member.person.full_name} - {self.ministry.name}"

    def clean(self):
        """Validates business rules for ministry participation"""
        super().clean()
        
        # Rule 1: Member must be active
        if not self.member.is_active:
            raise ValidationError({
                'member': 'Não é possível adicionar um membro inativo ao ministério'
            })
        
        # Rule 2: End date must be after start date
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({
                'end_date': 'Data de término não pode ser anterior à data de início'
            })
        
        # Rule 3: Ministry should be active? (optional - depends on Ministry model)
        if hasattr(self.ministry, 'is_active') and not self.ministry.is_active:
            raise ValidationError({
                'ministry': 'Não é possível adicionar membro a um ministério inativo'
            })

    def save(self, *args, **kwargs):
        """Performs validation and auto-sets end_date when deactivated"""
        if not self.is_active and not self.end_date:
            from datetime import date
            self.end_date = date.today()
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def duration_days(self):
        """Returns the duration of this ministry participation in days"""
        from datetime import date
        end = self.end_date if self.end_date else date.today()
        return (end - self.start_date).days
    
    @property
    def member_name(self):
        """Returns the member's full name"""
        return self.member.person.full_name
    
    @property
    def ministry_name(self):
        """Returns the ministry name"""
        return self.ministry.name
    
    @property
    def status_display(self):
        """Returns a user-friendly status string"""
        if self.is_active:
            return "Ativo"
        return f"Encerrado em {self.end_date.strftime('%d/%m/%Y') if self.end_date else 'N/A'}"
