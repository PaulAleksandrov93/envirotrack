from rest_framework import serializers
from .models import Responsible, Room, EnviromentalParameters


class ResponsibleSerializer(serializers.ModelSerializer):
    profession = serializers.StringRelatedField()
    class Meta:
        model = Responsible
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number']

class ResposibleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsible
        fields = ['first_name', 'last_name']


class EnvironmentalParametersSerializer(serializers.ModelSerializer):
    room = RoomNumberSerializer()
    responsible = ResposibleNameSerializer()

    class Meta:
        model = EnviromentalParameters
        fields = ['id', 'room', 'temperature_celsius', 'humidity_percentage', 'pressure_kpa', 'pressure_mmhg', 'date_time', 'responsible']