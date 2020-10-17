from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VesselSerializer, EquipmentSerializer

from .models import Equipment

# Create your views here.
