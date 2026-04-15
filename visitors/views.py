from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


class VisitorListView(ListView):
    model = models.Visitor
    template_name = 'visitor_list.html'
    context_object_name = 'visitors'

    def get_queryset(self):
        queryset = super().get_queryset()
        person_name = self.request.GET.get('person_name')

        if person_name:
            queryset = queryset.filter(person__full_name__icontains=person_name)

        return queryset


class VisitorCreateView(CreateView):
    model = models.Visitor
    template_name = 'visitor_create.html'
    form_class = forms.VisitorForm
    success_url = reverse_lazy('visitor_list')


class VisitorDetailView(DetailView):
    model = models.Visitor
    template_name = 'visitor_detail.html'
    context_object_name = 'visitor'


class VisitorUpdateView(UpdateView):
    model = models.Visitor
    template_name = 'visitor_update.html'
    form_class = forms.VisitorForm
    context_object_name = 'visitor'
    success_url = reverse_lazy('visitor_list')


class VisitorDeleteView(DeleteView):
    model = models.Visitor
    template_name = 'visitor_delete.html'
    success_url = reverse_lazy('visitor_list')
