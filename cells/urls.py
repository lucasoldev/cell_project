from django.urls import path
from . import views


urlpatterns = [
    path('cells/list/', views.CellListView.as_view(), name='cell_list'),
    path('cells/create/', views.CellCreateView.as_view(), name='cell_create'),
    path('cells/<str:pk>/', views.CellDetailView.as_view(), name='cell_detail'),
    path('cells/<str:pk>/update/', views.CellUpdateView.as_view(), name='cell_update'),
    path('cells/<str:pk>/delete/', views.CellDeleteView.as_view(), name='cell_delete'),
]
