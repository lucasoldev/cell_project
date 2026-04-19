from django.urls import path

from . import views

urlpatterns = [
    path('persons/list/', views.PersonListView.as_view(), name='person_list'),
    path('persons/create/', views.PersonCreateView.as_view(), name='person_create'),
    path('persons/<str:pk>/detail/', views.PersonDetailView.as_view(), name='person_detail'),
    path('persons/<str:pk>/update/', views.PersonUpdateView.as_view(), name='person_update'),
    path('persons/<str:pk>/delete/', views.PersonDeleteView.as_view(), name='person_delete'),
]
