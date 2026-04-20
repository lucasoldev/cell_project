from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home_view, name='dashboard'),
    path('', include('areas.urls')),
    path('', include('person.urls')),
    path('', include('members.urls')),
    path('', include('hosts.urls')),
    path('', include('visitors.urls')),
    path('', include('cells.urls')),
    path('', include('cell_locations.urls')),
    path('', include('cell_members.urls')),
    path('', include('leaderships.urls')),
    path('', include('member_ministries.urls')),
    path('', include('calendar_events.urls')),
    path('', include('cell_meetings.urls')),
    path('', include('meeting_attendances.urls')),
    path('', include('monthly_attendances.urls')),
]
