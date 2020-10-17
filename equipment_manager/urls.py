from django.urls import path
from . import views

urlpatterns = [
    path('vessel/', views.vessels, name='register-vessel'),
    path('equipment/', views.equipmentList, name='list-equipment'),
]
