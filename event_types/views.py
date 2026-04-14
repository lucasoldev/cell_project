from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from . import models


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
