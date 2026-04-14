from django.urls import path
from . import views


urlpatterns = [
    path('leadership_roles/list/', views.LeadershipRoleListView.as_view(), name='leadership_role_list'),
    path('leadership_roles/create/', views.LeadershipRoleCreateView.as_view(), name='leadership_role_create'),
    path('leadership_roles/<str:pk>/detail/', views.LeadershipRoleDetailView.as_view(), name='leadership_role_detail'),
    path('leadership_roles/<str:pk>/update/', views.LeadershipRoleUpdateView.as_view(), name='leadership_role_update'),
    path('leadership_roles/<str:pk>/delete/', views.LeadershipRoleDeleteView.as_view(), name='leadership_role_delete'),
]