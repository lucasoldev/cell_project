from django.db import models
from app.basemodel import BaseModel


class Ministry(BaseModel):
    """
    Church ministries
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'ministry'
        verbose_name_plural = 'ministries'
        ordering = ['name']

    def __str__(self):
        return self.name
