import json

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from hosts.models import Host

from . import forms, models


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Busca todos os anfitriões
        hosts = Host.objects.select_related('person').all()
        hosts_data = []

        for host in hosts:
            # Busca em QUAIS células este anfitrião JÁ É ANFITRIÃO (tem local cadastrado)
            hosted_cells = models.CellLocation.objects.filter(
                host=host
            ).values_list('cell_id', flat=True)

            hosts_data.append({
                'pk': str(host.pk),
                'name': host.person.full_name,
                'full_address': host.full_address,
                'hosted_cells': [str(cell_id) for cell_id in hosted_cells],  # Células onde já é anfitrião
            })

        context['all_hosts_json'] = json.dumps(hosts_data)
        return context


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
