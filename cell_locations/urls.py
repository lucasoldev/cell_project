from django.urls import path
from . import views


urlpatterns = [
    path('cell_locations/list/', views.CellLocationListView.as_view(), name='cell_location_list'),
    path('cell_locations/create/', views.CellLocationCreateView.as_view(), name='cell_location_create'),
    path('cell_locations/<str:pk>/', views.CellLocationDetailView.as_view(), name='cell_location_detail'),
    path('cell_locations/<str:pk>/update/', views.CellLocationUpdateView.as_view(), name='cell_location_update'),
    path('cell_locations/<str:pk>/delete/', views.CellLocationDeleteView.as_view(), name='cell_location_delete'),
]
