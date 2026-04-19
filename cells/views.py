from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from . import forms, models


class CellListView(ListView):
    model = models.Cell
    template_name = 'cell_list.html'
    context_object_name = 'cells'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class CellCreateView(CreateView):
    model = models.Cell
    template_name = 'cell_create.html'
    form_class = forms.CellForm
    success_url = reverse_lazy('cell_list')


class CellDetailView(DetailView):
    model = models.Cell
    template_name = 'cell_detail.html'
    context_object_name = 'cell'


class CellUpdateView(UpdateView):
    model = models.Cell
    template_name = 'cell_update.html'
    form_class = forms.CellForm
    context_object_name = 'cell'
    success_url = reverse_lazy('cell_list')

class CellDeleteView(DeleteView):
    model = models.Cell
    template_name = 'cell_delete.html'
    success_url = reverse_lazy('cell_list')
