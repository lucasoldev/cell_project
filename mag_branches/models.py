from django.db import models
from app.basemodel import BaseModel


class MagBranch(BaseModel):
    """
    MAG Branches (Mag, OW, A2)
    """
    class MagBranchName(models.TextChoices):
        A2 = 'A2', 'A2'
        OW = 'OW', 'OW'
        MAG = 'MAG', 'MAG'

    name = models.CharField(
        max_length=20,
        choices=MagBranchName.choices,
        unique=True
    )
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'mag_branch'
        verbose_name = 'MAG Branch'
        verbose_name_plural = 'MAG Branches'
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()