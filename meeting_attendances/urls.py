from django.urls import path
from . import views


urlpatterns = [
    path('meeting_attendances/list/', views.MeetingAttendanceListView.as_view(), name='meeting_attendance_list'),
    path('meeting_attendances/create/', views.MeetingAttendanceCreateView.as_view(), name='meeting_attendance_create'),
    path('meeting_attendances/<str:pk>/', views.MeetingAttendanceDetailView.as_view(), name='meeting_attendance_detail'),
    path('meeting_attendances/<str:pk>/update/', views.MeetingAttendanceUpdateView.as_view(), name='meeting_attendance_update'),
    path('meeting_attendances/<str:pk>/delete/', views.MeetingAttendanceDeleteView.as_view(), name='meeting_attendance_delete'),
]
