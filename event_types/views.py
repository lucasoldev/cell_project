from django.views.generic import ListView
from . import models


class EventTypeListView(ListView):
    model = models.EventType
    template_name = 'event_types_list.html'
    context_object_name = 'event_types'
