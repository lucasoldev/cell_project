from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


class CellMeetingListView(ListView):
    model = models.CellMeeting
    template_name = 'cell_meeting_list.html'
    context_object_name = 'cell_meetings'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        cell_name = self.request.GET.get('cell_name')
        took_place = self.request.GET.get('took_place')

        if cell_name:
            queryset = queryset.filter(cell__name__icontains=cell_name)

        if took_place:
            queryset = queryset.filter(took_place=took_place == 'true')

        return queryset.select_related(
            'cell__area', 'cell_location__host__person', 'calendar_event__event_type'
        )


class CellMeetingCreateView(CreateView):
    model = models.CellMeeting
    template_name = 'cell_meeting_create.html'
    form_class = forms.CellMeetingForm
    success_url = reverse_lazy('cell_meeting_list')


class CellMeetingDetailView(DetailView):
    model = models.CellMeeting
    template_name = 'cell_meeting_detail.html'
    context_object_name = 'cell_meeting'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'cell__area', 'cell_location__host__person', 'calendar_event__event_type'
        )


class CellMeetingUpdateView(UpdateView):
    model = models.CellMeeting
    template_name = 'cell_meeting_update.html'
    form_class = forms.CellMeetingForm
    context_object_name = 'cell_meeting'
    success_url = reverse_lazy('cell_meeting_list')


class CellMeetingDeleteView(DeleteView):
    model = models.CellMeeting
    template_name = 'cell_meeting_delete.html'
    success_url = reverse_lazy('cell_meeting_list')
