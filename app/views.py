from datetime import date, timedelta
from django.shortcuts import render
from django.db.models import Count, Q, Avg
from django.contrib.auth.decorators import login_required

from cells.models import Cell
from members.models import Member
from visitors.models import Visitor
from cell_meetings.models import CellMeeting
from meeting_attendances.models import MeetingAttendance
from monthly_attendances.models import MonthlyAttendance
from cell_members.models import CellMember
from leaderships.models import Leadership
from django.shortcuts import render


def home_view(request):
    return render(request, 'dashboard.html')


@login_required
def dashboard_view(request):
    """Dashboard view with key metrics and charts"""
    today = date.today()
    first_day_of_month = today.replace(day=1)
    thirty_days_ago = today - timedelta(days=30)
    
    # ========== MÉTRICAS PRINCIPAIS ==========
    total_cells = Cell.objects.count()
    active_cells = Cell.objects.filter(
        locations__is_active=True
    ).distinct().count()
    
    total_members = Member.objects.count()
    active_members = Member.objects.filter(is_active=True).count()
    
    monthly_visitors = Visitor.objects.filter(
        visit_date__gte=first_day_of_month
    ).count()
    
    converted_visitors = Visitor.objects.filter(
        visit_date__gte=first_day_of_month,
        became_member=True
    ).count()
    
    conversion_rate = (converted_visitors / monthly_visitors * 100) if monthly_visitors > 0 else 0
    
    # Presença média nos últimos 30 dias
    avg_attendance = MeetingAttendance.objects.filter(
        cell_meeting__meeting_date__gte=thirty_days_ago,
        attended=True
    ).aggregate(
        avg=Avg('cell_meeting__total_attendees')
    )['avg'] or 0
    
    # ========== DADOS PARA GRÁFICOS ==========
    
    # 1. Presença semanal (últimas 4 semanas)
    weekly_attendance_data = get_weekly_attendance_data()
    
    # 2. Novos membros por mês (últimos 6 meses)
    monthly_new_members_data = get_monthly_new_members_data()
    
    # 3. Células por área
    cells_by_area = dict(
        Cell.objects.values('area__color').annotate(
            count=Count('id')
        ).values_list('area__color', 'count')
    )
    
    # 4. Membros por célula (top 5)
    members_by_cell = list(
        CellMember.objects.filter(is_active=True).values('cell__name').annotate(
            count=Count('member', distinct=True)
        ).order_by('-count')[:5]
    )
    
    # 5. Fidelidade mensal
    faithful_count = MonthlyAttendance.objects.filter(
        year=today.year,
        month=today.month,
        is_faithful=True
    ).count()
    unfaithful_count = MonthlyAttendance.objects.filter(
        year=today.year,
        month=today.month,
        is_faithful=False,
        total_meetings__gt=0
    ).count()
    
    # ========== PRÓXIMAS REUNIÕES ==========
    upcoming_meetings = CellMeeting.objects.filter(
        meeting_date__gte=today,
        took_place=False
    ).select_related(
        'cell', 'cell_location__host__person'
    ).order_by('meeting_date')[:5]
    
    # ========== MEMBROS FIÉIS DO MÊS ==========
    faithful_members = MonthlyAttendance.objects.filter(
        year=today.year,
        month=today.month,
        is_faithful=True,
        total_meetings__gt=0
    ).select_related(
        'member__person', 'cell'
    ).order_by('-attendance_percentage')[:10]
    
    context = {
        # Métricas principais
        'total_cells': total_cells,
        'active_cells': active_cells,
        'total_members': total_members,
        'active_members': active_members,
        'monthly_visitors': monthly_visitors,
        'conversion_rate': round(conversion_rate, 1),
        'avg_attendance': round(avg_attendance, 1),
        
        # Dados para gráficos (convertidos para JSON no template)
        'weekly_attendance_data': weekly_attendance_data,
        'monthly_new_members_data': monthly_new_members_data,
        'cells_by_area': cells_by_area,
        'members_by_cell': members_by_cell,
        'faithful_count': faithful_count,
        'unfaithful_count': unfaithful_count,
        
        # Listas
        'upcoming_meetings': upcoming_meetings,
        'faithful_members': faithful_members,
    }
    
    return render(request, 'dashboard.html', context)


def get_weekly_attendance_data():
    """Retorna dados de presença das últimas 4 semanas"""
    today = date.today()
    weeks = []
    
    for i in range(3, -1, -1):
        week_start = today - timedelta(days=today.weekday() + 7 * i)
        week_end = week_start + timedelta(days=6)
        weeks.append({
            'label': f"{week_start.strftime('%d/%m')} - {week_end.strftime('%d/%m')}",
            'start': week_start,
            'end': week_end,
        })
    
    labels = [w['label'] for w in weeks]
    values = []
    
    for week in weeks:
        attendance_count = MeetingAttendance.objects.filter(
            cell_meeting__meeting_date__gte=week['start'],
            cell_meeting__meeting_date__lte=week['end'],
            attended=True
        ).count()
        values.append(attendance_count)
    
    return {'labels': labels, 'values': values}


def get_monthly_new_members_data():
    """Retorna dados de novos membros nos últimos 6 meses"""
    today = date.today()
    months = []
    values = []
    
    for i in range(5, -1, -1):
        month_date = today.replace(day=1) - timedelta(days=30 * i)
        month_date = month_date.replace(day=1)
        
        count = Member.objects.filter(
            entry_date__year=month_date.year,
            entry_date__month=month_date.month
        ).count()
        
        months.append(month_date.strftime('%b/%Y'))
        values.append(count)
    
    return {'labels': months, 'values': values}