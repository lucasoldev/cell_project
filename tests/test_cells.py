import pytest
from django.core.exceptions import ValidationError

from areas.models import Area
from cells.models import Cell
from mag_branches.models import MagBranch


@pytest.mark.django_db
def test_mag_cell_requires_a_branch():
    mag_area = Area.objects.create(is_mag=True)
    cell = Cell(name='Célula MAG', area=mag_area)

    with pytest.raises(ValidationError) as raised:
        cell.save()

    assert 'mag_branch' in raised.value.message_dict
    assert not Cell.objects.filter(name='Célula MAG').exists()


@pytest.mark.django_db
def test_non_mag_cell_rejects_a_branch():
    area = Area.objects.create(color=Area.AreaColor.AZUL)
    branch = MagBranch.objects.create(name=MagBranch.MagBranchName.MAG)
    cell = Cell(name='Célula Azul', area=area, mag_branch=branch)

    with pytest.raises(ValidationError) as raised:
        cell.save()

    assert 'mag_branch' in raised.value.message_dict
    assert not Cell.objects.filter(name='Célula Azul').exists()


@pytest.mark.django_db
def test_mag_cell_with_branch_is_saved():
    mag_area = Area.objects.create(is_mag=True)
    branch = MagBranch.objects.create(name=MagBranch.MagBranchName.MAG)

    cell = Cell.objects.create(
        name='Célula MAG válida', area=mag_area, mag_branch=branch
    )

    assert Cell.objects.get(pk=cell.pk).mag_branch == branch
