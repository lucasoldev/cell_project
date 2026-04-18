from django.urls import path
from . import views


urlpatterns = [
    path('calendar_events/list/', views.CalendarEventListView.as_view(), name='calendar_event_list'),
    path('calendar_events/create/', views.CalendarEventCreateView.as_view(), name='calendar_event_create'),
    path('calendar_events/<str:pk>/', views.CalendarEventDetailView.as_view(), name='calendar_event_detail'),
    path('calendar_events/<str:pk>/update/', views.CalendarEventUpdateView.as_view(), name='calendar_event_update'),
    path('calendar_events/<str:pk>/delete/', views.CalendarEventDeleteView.as_view(), name='calendar_event_delete'),
]
