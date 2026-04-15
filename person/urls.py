from django.urls import path
from . import views


urlpatterns = [
    path('person/list/', views.PersonListView.as_view(), name='person_list'),
    path('person/create/', views.PersonCreateView.as_view(), name='person_create'),
    path('person/<str:pk>/detail/', views.PersonDetailView.as_view(), name='person_detail'),
    path('person/<str:pk>/update/', views.PersonUpdateView.as_view(), name='person_update'),
    path('person/<str:pk>/delete/', views.PersonDeleteView.as_view(), name='person_delete'),
]