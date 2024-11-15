from django.urls import path
from . import views

urlpatterns = [
    path('', views.favorit, name='favorit'),  
]

