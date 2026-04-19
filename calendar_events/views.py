from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from . import forms, models


class CalendarEventListView(ListView):
    model = models.CalendarEvent
    template_name = 'calendar_event_list.html'
    context_object_name = 'calendar_events'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        event_type = self.request.GET.get('event_type')
        search = self.request.GET.get('search')

        if event_type:
            queryset = queryset.filter(event_type__name=event_type)

        if search:
            queryset = queryset.filter(description__icontains=search)

        return queryset.select_related('event_type')


class CalendarEventCreateView(CreateView):
    model = models.CalendarEvent
    template_name = 'calendar_event_create.html'
    form_class = forms.CalendarEventForm
    success_url = reverse_lazy('calendar_event_list')


class CalendarEventDetailView(DetailView):
    model = models.CalendarEvent
    template_name = 'calendar_event_detail.html'
    context_object_name = 'calendar_event'
    success_url = reverse_lazy('calendar_event_list')


class CalendarEventUpdateView(UpdateView):
    model = models.CalendarEvent
    template_name = 'calendar_event_update.html'
    form_class = forms.CalendarEventForm
    context_object_name = 'calendar_event'
    success_url = reverse_lazy('calendar_event_list')


class CalendarEventDeleteView(DeleteView):
    model = models.CalendarEvent
    template_name = 'calendar_event_delete.html'
    success_url = reverse_lazy('calendar_event_list')
