from django.views.generic import DetailView, ListView

from . import models


class MonthlyAttendanceListView(ListView):
    """
    List view for MonthlyAttendance records.
    """
    model = models.MonthlyAttendance
    template_name = 'monthly_attendance_list.html'
    context_object_name = 'monthly_attendance_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtros
        member_name = self.request.GET.get('member_name')
        cell_name = self.request.GET.get('cell_name')
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        is_faithful = self.request.GET.get('is_faithful')

        if member_name:
            queryset = queryset.filter(member__person__full_name__icontains=member_name)
        if cell_name:
            queryset = queryset.filter(cell__name__icontains=cell_name)
        if year:
            queryset = queryset.filter(year=year)
        if month:
            queryset = queryset.filter(month=month)
        if is_faithful in ['true', 'false']:
            queryset = queryset.filter(is_faithful=is_faithful == 'true')

        return queryset.select_related('member__person', 'cell__area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lista de anos disponíveis (do ano atual até 2020)
        from datetime import date
        current_year = date.today().year
        context['years'] = range(current_year, 2019, -1)

        return context


class MonthlyAttendanceDetailView(DetailView):
    """
    Detail view for MonthlyAttendance records.
    """
    model = models.MonthlyAttendance
    template_name = 'monthly_attendance_detail.html'
    context_object_name = 'monthly_attendance_detail'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'member__person',
            'cell__area'
        )
