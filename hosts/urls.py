from django.urls import path

from . import views

urlpatterns = [
    path('hosts/list/', views.HostListView.as_view(), name='host_list'),
    path('hosts/create/', views.HostCreateView.as_view(), name='host_create'),
    path('hosts/<str:pk>/', views.HostDetailView.as_view(), name='host_detail'),
    path('hosts/<str:pk>/update/', views.HostUpdateView.as_view(), name='host_update'),
    path('hosts/<str:pk>/delete/', views.HostDeleteView.as_view(), name='host_delete'),
]
