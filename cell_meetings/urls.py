from django.urls import path

from . import views

urlpatterns = [
    path('cell_meetings/list/', views.CellMeetingListView.as_view(), name='cell_meeting_list'),
    path('cell_meetings/create/', views.CellMeetingCreateView.as_view(), name='cell_meeting_create'),
    path('cell_meetings/attendance-report/', views.attendance_report_select_cell, name='attendance_report_select'),
    path('cell_meetings/save-attendance/', views.save_attendance, name='save_attendance'),
    
    path('cell_meetings/cell/<str:cell_pk>/attendance-grid/', views.monthly_attendance_grid, name='monthly_attendance_grid'),
    path('cell_meetings/<str:pk>/', views.CellMeetingDetailView.as_view(), name='cell_meeting_detail'),
    path('cell_meetings/<str:pk>/update/', views.CellMeetingUpdateView.as_view(), name='cell_meeting_update'),
    path('cell_meetings/<str:pk>/delete/', views.CellMeetingDeleteView.as_view(), name='cell_meeting_delete'),
]