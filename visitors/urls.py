from django.urls import path
from . import views


urlpatterns = [
    path('visitors/list/', views.VisitorListView.as_view(), name='visitor_list'),
    path('visitors/create/', views.VisitorCreateView.as_view(), name='visitor_create'),
    path('visitors/<str:pk>/', views.VisitorDetailView.as_view(), name='visitor_detail'),
    path('visitors/<str:pk>/update/', views.VisitorUpdateView.as_view(), name='visitor_update'),
    path('visitors/<str:pk>/delete/', views.VisitorDeleteView.as_view(), name='visitor_delete'),
]
