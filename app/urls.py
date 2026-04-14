from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('event_types.urls')),
    path('', include('leadership_roles.urls')),
]
