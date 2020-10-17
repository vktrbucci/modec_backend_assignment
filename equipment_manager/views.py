from django.shortcuts import render

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from .serializers import VesselSerializer, EquipmentSerializer
from .models import Equipment, Vessel

# Create your views here.

@api_view(['GET', 'POST'])
def vessels(request):
    if request.method == 'GET':
        vessels = Vessel.objects.all()

        vessel_code = request.query_params.get('code', None)
        if vessel_code is not None:
            vessels = vessels.filter(vessels__icontains=vessel_code)

        vessels_serializer = VesselSerializer(vessels, many=True)
        return JsonResponse(vessels_serializer.data, safe=False)

    elif request.method == 'POST':
        vessel_data = JSONParser().parse(request)
        vessel_serializer = VesselSerializer(data=vessel_data)

        if vessel_serializer.is_valid():
            vessel_serializer.save()
            return JsonResponse(vessel_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(vessel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT'])
def equipmentList(request):
    if request.method == 'GET':
        activeEquipment = Equipment.objects.all()

