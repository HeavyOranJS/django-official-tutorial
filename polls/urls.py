from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    #just checking what will happen
    path('testo', views.index, name = 'testo')
]