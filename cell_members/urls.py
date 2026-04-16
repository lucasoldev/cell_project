from django.urls import path
from . import views


urlpatterns = [
    path('cell_members/list/', views.CellMemberListView.as_view(), name='cell_member_list'),
    path('cell_members/create/', views.CellMemberCreateView.as_view(), name='cell_member_create'),
    path('cell_members/<str:pk>/', views.CellMemberDetailView.as_view(), name='cell_member_detail'),
    path('cell_members/<str:pk>/update/', views.CellMemberUpdateView.as_view(), name='cell_member_update'),
    path('cell_members/<str:pk>/delete/', views.CellMemberDeleteView.as_view(), name='cell_member_delete'),
]
