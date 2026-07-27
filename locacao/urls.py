from django.urls import path 
from locacao import views


urlpatterns = [
    path('', views.list_location, name='list-location'), 
    path('form_client/', views.form_client, name='client-create'),
    path('list_client/', views.list_client, name='list-client'),
    path('update_client/<int:id>/', views.update_client, name='client-update'),
    path('delete_client/<int:id>/', views.delete_client, name='client-delete'),
    path('form_immobile/', views.form_immobile, name='immobile-create'),
    path('list_immobile/', views.list_immobile, name='list-immobile'),
    path('update_immobile/<int:id>/', views.update_immobile, name='immobile-update'),
    path('delete_immobile/<int:id>/', views.delete_immobile, name='immobile-delete'),
    path('form_location/<int:id>/', views.form_location, name='location-create'),
    path('list_locations/', views.list_location_register, name='list-locations'),
    path('finish_location/<int:id>/', views.finish_location, name='location-finish'),
    path('reports/', views.reports, name='reports'),
]