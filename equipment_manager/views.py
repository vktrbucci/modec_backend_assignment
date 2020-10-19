from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from .serializers import VesselSerializer, EquipmentSerializer
from .models import Equipment, Vessel

# Create your views here.

@api_view(['POST'])
def vessel(request):
    if request.method == 'POST':
        vessel = JSONParser().parse(request)
        serializer = VesselSerializer(data=vessel)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', 'PATCH'])
def equipment(request):
    if request.method == 'POST':
        equipment = JSONParser().parse(request)
        serializer = EquipmentSerializer(data=equipment)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        equipment = JSONParser().parse(request)
        serializer = EquipmentSerializer(data=equipment, partial=True)

        if serializer.is_valid():
            serializer.update()

            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def vesselEquipment(request, pk):
    try:
        vessel = Vessel.objects.get(pk=pk)
    except:
        return JsonResponse({"message": "This vessel does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        equipment = Equipment.objects.filter(vessel=pk, status=True)
        serializer = EquipmentSerializer(equipment, many=True)

        if serializer.data == []:
            return JsonResponse({"message": "There is no active equipment in this vessel."}, status=status.HTTP_404_NOT_FOUND)
        
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    return JsonResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

