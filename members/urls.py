from django.urls import path
from . import views


urlpatterns = [
    path('members/list/', views.MemberListView.as_view(), name='member_list'),
    path('members/create/', views.MemberCreateView.as_view(), name='member_create'),
    path('members/<str:pk>/detail/', views.MemberDetailView.as_view(), name='member_detail'),
    path('members/<str:pk>/update/', views.MemberUpdateView.as_view(), name='member_update'),
    path('members/<str:pk>/delete/', views.MemberDeleteView.as_view(), name='member_delete'),
]