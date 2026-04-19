from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from . import forms, models


class PersonListView(ListView):
    model = models.Person
    template_name = 'person_list.html'
    context_object_name = 'persons'

    def get_queryset(self):
        queryset = super().get_queryset()
        full_name = self.request.GET.get('full_name')

        if full_name:
            queryset = queryset.filter(full_name__icontains=full_name)

        return queryset


class PersonCreateView(CreateView):
    model = models.Person
    template_name = 'person_create.html'
    form_class = forms.PersonForm
    success_url = reverse_lazy('person_list')


class PersonDetailView(DetailView):
    model = models.Person
    template_name = 'person_detail.html'
    context_object_name = 'person'


class PersonUpdateView(UpdateView):
    model = models.Person
    template_name = 'person_update.html'
    form_class = forms.PersonForm
    context_object_name = 'person'
    success_url = reverse_lazy('person_list')


class PersonDeleteView(DeleteView):
    model = models.Person
    template_name = 'person_delete.html'
    success_url = reverse_lazy('person_list')
