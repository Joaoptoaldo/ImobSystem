from django.urls import path 
from apps import views

urlpatterns = [
    path('', views.mysite, name='mysite'), 
]