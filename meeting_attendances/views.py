from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from . import forms, models


class MeetingAttendanceListView(ListView):
    model = models.MeetingAttendance
    template_name = 'meeting_attendance_list.html'
    context_object_name = 'attendances'

    def get_queryset(self):
        queryset = super().get_queryset()
        member_name = self.request.GET.get('member_name')

        if member_name:
            queryset = queryset.filter(
                member__person__full_name__icontains=member_name
            )

        return queryset.select_related(
            'cell_meeting__cell', 'member__person'
        )


class MeetingAttendanceCreateView(CreateView):
    model = models.MeetingAttendance
    template_name = 'meeting_attendance_create.html'
    form_class = forms.MeetingAttendanceForm
    success_url = reverse_lazy('meeting_attendance_list')


class MeetingAttendanceDetailView(DetailView):
    model = models.MeetingAttendance
    template_name = 'meeting_attendance_detail.html'
    context_object_name = 'attendance'
    success_url = reverse_lazy('meeting_attendance_list')


class MeetingAttendanceUpdateView(UpdateView):
    model = models.MeetingAttendance
    template_name = 'meeting_attendance_update.html'
    form_class = forms.MeetingAttendanceForm
    context_object_name = 'attendance'
    success_url = reverse_lazy('meeting_attendance_list')

    def get_queryset(self):
        return super().get_queryset().select_related(
            'cell_meeting__cell', 'member__person'
        )


class MeetingAttendanceDeleteView(DeleteView):
    model = models.MeetingAttendance
    template_name = 'meeting_attendance_delete.html'
    success_url = reverse_lazy('meeting_attendance_list')
