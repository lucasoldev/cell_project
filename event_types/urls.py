from django.urls import path
from . import views


urlpatterns = [
    path('event_types/list/', views.EventTypeListView.as_view(), name='event_type_list'),
    path('event_types/create/', views.EventTypeCreateView.as_view(), name='event_type_create'),
    path('event_types/<str:pk>/detail/', views.EventTypeDetailView.as_view(), name='event_type_detail'),
    path('event_types/<str:pk>/update/', views.EventTypeUpdateView.as_view(), name='event_type_update'),
    path('event_types/<str:pk>/delete/', views.EventTypeDeleteView.as_view(), name='event_type_delete'),
]