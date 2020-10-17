from rest_framework import serializers
from .models import Vessel, Equipment


class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = (
            'id',
            'code',
        )


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = (
            'id',
            'name',
            'code',
            'location',
            'vessel',
            'status',
        )
