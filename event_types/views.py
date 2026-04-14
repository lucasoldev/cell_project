from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from . import models, forms


class EventTypeListView(ListView):
    model = models.EventType
    template_name = 'event_types_list.html'
    context_object_name = 'event_types'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset


class EventTypeCreateView(CreateView):
    model = models.EventType
    template_name = 'event_types_create.html'
    form_class = forms.EventTypeForm
    success_url = reverse_lazy('event_type_list')
    context_object_name = 'event_types_create'
