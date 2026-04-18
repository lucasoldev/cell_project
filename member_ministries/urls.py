from django.urls import path
from . import views

urlpatterns = [
    path('member_ministries/list/', views.MemberMinistryListView.as_view(), name='member_ministry_list'),
    path('member_ministries/create/', views.MemberMinistryCreateView.as_view(), name='member_ministry_create'),
    path('member_ministries/<str:pk>/', views.MemberMinistryDetailView.as_view(), name='member_ministry_detail'),
    path('member_ministries/<str:pk>/update/', views.MemberMinistryUpdateView.as_view(), name='member_ministry_update'),
    path('member_ministries/<str:pk>/delete/', views.MemberMinistryDeleteView.as_view(), name='member_ministry_delete'),
]
