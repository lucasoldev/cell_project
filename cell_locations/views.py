from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


class CellLocationListView(ListView):
    model = models.CellLocation
    template_name = 'cell_location_list.html'
    context_object_name = 'cell_locations'

    def get_queryset(self):
        queryset = super().get_queryset()
        cell_name = self.request.GET.get('cell_name')

        if cell_name:
            queryset = queryset.filter(cell__name__icontains=cell_name)

        return queryset


class CellLocationCreateView(CreateView):
    model = models.CellLocation
    template_name = 'cell_location_create.html'
    form_class = forms.CellLocationForm
    success_url = reverse_lazy('cell_location_list')


class CellLocationDetailView(DetailView):
    model = models.CellLocation
    template_name = 'cell_location_detail.html'
    context_object_name = 'cell_location'


class CellLocationUpdateView(UpdateView):
    model = models.CellLocation
    template_name = 'cell_location_update.html'
    form_class = forms.CellLocationForm
    context_object_name = 'cell_location'
    success_url = reverse_lazy('cell_location_list')


class CellLocationDeleteView(DeleteView):
    model = models.CellLocation
    template_name = 'cell_location_delete.html'
    success_url = reverse_lazy('cell_location_list')
