from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from cells.models import Cell
from cell_members.models import CellMember
from visitors.models import Visitor
from meeting_attendances.models import MeetingAttendance
from members.models import Member

from . import forms, models


# ========== CRUD VIEWS (EXISTING) ==========

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


# ========== ATTENDANCE GRID (NEW VIEWS) ==========

@login_required
def monthly_attendance_grid(request, cell_pk):
    """Displays the monthly attendance grid for a cell"""

    cell = get_object_or_404(Cell, pk=cell_pk)

    # Define month/year (default: current month)
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # First and last day of the month
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year, month, 31)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    # Fetch all meetings for this cell in this month
    meetings = models.CellMeeting.objects.filter(
        cell=cell,
        meeting_date__gte=first_day,
        meeting_date__lte=last_day,
        took_place=True
    ).order_by('meeting_date')

    # Fetch active members of the cell
    cell_members = CellMember.objects.filter(
        cell=cell,
        is_active=True
    ).select_related('member__person').order_by('member__person__full_name')

    # Fetch visitors for the month (who visited this cell)
    visitors = Visitor.objects.filter(
        cell=cell,
        visit_date__gte=first_day,
        visit_date__lte=last_day
    ).select_related('person').order_by('person__full_name')

    # Prepare grid data
    attendance_data = []

    # Add members
    for cell_member in cell_members:
        row = {
            'id': f'member_{cell_member.member.pk}',
            'name': cell_member.member.person.full_name,
            'type': 'member',
            'type_label': 'Member',
            'attendances': {}
        }

        # Fetch already recorded attendances
        for meeting in meetings:
            attendance = MeetingAttendance.objects.filter(
                cell_meeting=meeting,
                member=cell_member.member
            ).first()
            row['attendances'][meeting.pk] = attendance.attended if attendance else False

        attendance_data.append(row)

    # Add visitors
    for visitor in visitors:
        row = {
            'id': f'visitor_{visitor.pk}',
            'name': visitor.person.full_name,
            'type': 'visitor',
            'type_label': 'Visitor',
            'attendances': {}
        }

        # Visitors don't have attendance recorded (view only)
        for meeting in meetings:
            row['attendances'][meeting.pk] = None

        attendance_data.append(row)

    # Month navigation
    prev_month = first_day - timedelta(days=1)
    next_month = last_day + timedelta(days=1)

    context = {
        'cell': cell,
        'year': year,
        'month': month,
        'month_name': first_day.strftime('%B/%Y'),
        'meetings': meetings,
        'attendance_data': attendance_data,
        'prev_month': {'year': prev_month.year, 'month': prev_month.month},
        'next_month': {'year': next_month.year, 'month': next_month.month},
        'months': [
            (1, 'January'), (2, 'February'), (3, 'March'),
            (4, 'April'), (5, 'May'), (6, 'June'),
            (7, 'July'), (8, 'August'), (9, 'September'),
            (10, 'October'), (11, 'November'), (12, 'December')
        ],
    }

    return render(request, 'monthly_attendance_grid.html', context)


@login_required
def save_attendance(request):
    """Saves attendances via AJAX (accepts batch)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    import json
    
    # Try to get data as JSON first (for batch)
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            attendances = data.get('attendances', [])
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        # Single mode (compatibility with individual checkbox)
        meeting_id = request.POST.get('meeting_id')
        member_id = request.POST.get('member_id')
        attended = request.POST.get('attended') == 'true'
        attendances = [{
            'meeting_id': meeting_id,
            'member_id': member_id,
            'attended': attended
        }]

    try:
        with transaction.atomic():
            results = []
            for item in attendances:
                meeting = models.CellMeeting.objects.get(pk=item['meeting_id'])
                member = Member.objects.get(pk=item['member_id'])

                attendance, created = MeetingAttendance.objects.update_or_create(
                    cell_meeting=meeting,
                    member=member,
                    defaults={'attended': item['attended']}
                )
                results.append({
                    'meeting_id': item['meeting_id'],
                    'member_id': item['member_id'],
                    'success': True,
                    'attended': attendance.attended
                })

        return JsonResponse({'success': True, 'results': results})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def attendance_report_select_cell(request):
    """Screen to select a cell and view the attendance grid"""
    from cells.models import Cell
    cells = Cell.objects.all().order_by('name')
    return render(request, 'select_cell_for_attendance.html', {'cells': cells})
