from django.urls import path 
from locacao import views


urlpatterns = [
    path('', views.list_location, name='list-location'), 
    path('form_client/', views.form_client, name='client-create'),
    path('form_immobile/', views.form_immobile, name='immobile-create'),
    path('form_location/<int:id>/', views.form_location, name='location-create'),
    path('reports/', views.reports, name='reports'),
]