from django.urls import path
from . import views


urlpatterns = [
    path('event_types/list/', views.EventTypeListView.as_view(), name='event_type_list'),
    path('event_types/create/', views.EventTypeCreateView.as_view(), name='event_type_create'),
]