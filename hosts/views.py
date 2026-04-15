from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


class HostListView(ListView):
    model = models.Host
    template_name = 'host_list.html'
    context_object_name = 'hosts'

    def get_queryset(self):
        queryset = super().get_queryset()
        person_name = self.request.GET.get('person_name')

        if person_name:
            queryset = queryset.filter(person__full_name__icontains=person_name)
        
        return queryset


class HostCreateView(CreateView):
    model = models.Host
    template_name = 'host_create.html'
    form_class = forms.HostForm
    success_url = reverse_lazy('host_list')


class HostDetailView(DetailView):
    model = models.Host
    template_name = 'host_detail.html'
    context_object_name = 'host'


class HostUpdateView(UpdateView):
    model = models.Host
    template_name = 'host_update.html'
    form_class = forms.HostForm
    context_object_name = 'host'
    success_url = reverse_lazy('host_list')


class HostDeleteView(DeleteView):
    model = models.Host
    template_name = 'host_delete.html'
    success_url = reverse_lazy('host_list')
