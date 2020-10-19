from django.urls import path
from . import views

urlpatterns = [
    path('vessel/', views.vessel, name='vessel'), 
    path('vessel/equipment/', views.equipment, name='equipment'),
    path('vessel/<int:pk>/', views.vesselEquipment, name='list-active-equipment'),
    # path('vessel/equipment/<pk>/', views.vesselEquipment, name='deactivate-equipment'),

]
