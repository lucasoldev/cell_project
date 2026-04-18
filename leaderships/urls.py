from django.urls import path
from . import views


urlpatterns = [
    path('leaderships/list/', views.LeadershipListView.as_view(), name='leadership_list'),
    path('leaderships/create/', views.LeadershipCreateView.as_view(), name='leadership_create'),
    path('leaderships/<str:pk>/', views.LeadershipDetailView.as_view(), name='leadership_detail'),
    path('leaderships/<str:pk>/update/', views.LeadershipUpdateView.as_view(), name='leadership_update'),
    path('leaderships/<str:pk>/delete/', views.LeadershipDeleteView.as_view(), name='leadership_delete'),
]
