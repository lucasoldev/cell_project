from django import forms

from . import models


class LeadershipRoleForm(forms.ModelForm):

    class Meta:
        model = models.LeadershipRole
        fields = ['title', 'description']
