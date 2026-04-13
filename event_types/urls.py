from django.urls import path
from . import views


urlpatterns = [
    path('event_types/list/', views.EventTypeListView.as_view(), name='event_type_list')
]