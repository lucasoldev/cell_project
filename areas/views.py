from django.views.generic import ListView, DetailView
from . import models


class AreaListView(ListView):
    """
    List view for Area records.
    """
    model = models.Area
    template_name = 'area_list.html'
    context_object_name = 'area_list'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        color = self.request.GET.get('color')
        is_mag = self.request.GET.get('is_mag')

        if color:
            queryset = queryset.filter(color__icontains=color)
        if is_mag in ['true', 'false']:
            queryset = queryset.filter(is_mag=is_mag == 'true')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Cores disponíveis para o filtro
        context['color_choices'] = models.Area.AreaColor.choices
        return context


class AreaDetailView(DetailView):
    """
    Detail view for Area records.
    """
    model = models.Area
    template_name = 'area_detail.html'
    context_object_name = 'area_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area = self.get_object()
        
        # Total de membros nas células desta área
        from cell_members.models import CellMember
        context['total_members'] = CellMember.objects.filter(
            cell__area=area,
            is_active=True
        ).count()
        
        # Total de reuniões este mês
        from datetime import date
        from cell_meetings.models import CellMeeting
        today = date.today()
        context['total_meetings'] = CellMeeting.objects.filter(
            cell__area=area,
            meeting_date__year=today.year,
            meeting_date__month=today.month,
            took_place=True
        ).count()
        
        return context
