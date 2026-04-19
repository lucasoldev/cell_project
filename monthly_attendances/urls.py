from django.urls import path
from . import views


urlpatterns = [
    path('monthly_attendances/list/', views.MonthlyAttendanceListView.as_view(), name='monthly_attendance_list'),
    path('monthly_attendances/<str:pk>/', views.MonthlyAttendanceDetailView.as_view(), name='monthly_attendance_detail'),
]
