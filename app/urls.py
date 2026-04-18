from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('person.urls')),
    path('', include('members.urls')),
    path('', include('hosts.urls')),
    path('', include('visitors.urls')),
    path('', include('cells.urls')),
    path('', include('cell_locations.urls')),
    path('', include('cell_members.urls')),
    path('', include('leaderships.urls')),
    path('', include('member_ministries.urls')),
]
