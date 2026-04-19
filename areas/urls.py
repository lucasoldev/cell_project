from django.urls import path

from . import views

urlpatterns = [
    path('areas/list/', views.AreaListView.as_view(), name='area_list'),
    path('areas/<str:pk>/', views.AreaDetailView.as_view(), name='area_detail'),
]
