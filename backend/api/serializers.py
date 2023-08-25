from rest_framework import serializers
from backend.models import Responsible, Room, EnviromentalParameters


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

class RoomSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number']

class ResposibleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsible
        fields = ['first_name', 'last_name']

class EnvironmentalParametersSerializer(serializers.ModelSerializer):
    room = RoomSelectSerializer()
    responsible = ResponsibleSerializer()  

    class Meta:
        model = EnviromentalParameters
        fields = ['id', 'room', 'temperature_celsius', 'humidity_percentage', 'pressure_kpa', 'pressure_mmhg', 'date_time', 'responsible']

    def update(self, instance, validated_data):
        room_data = validated_data.pop('room', None)
        responsible_data = validated_data.pop('responsible', None)

        if room_data:
            room, created = Room.objects.get_or_create(room_number=room_data.get('room_number'))
            instance.room = room

        if responsible_data:
            responsible, created = Responsible.objects.get_or_create(
                first_name=responsible_data.get('first_name'),
                last_name=responsible_data.get('last_name')
            )
            instance.responsible = responsible

        instance.temperature_celsius = validated_data.get('temperature_celsius', instance.temperature_celsius)
        instance.humidity_percentage = validated_data.get('humidity_percentage', instance.humidity_percentage)
        instance.pressure_kpa = validated_data.get('pressure_kpa', instance.pressure_kpa)
        instance.pressure_mmhg = validated_data.get('pressure_mmhg', instance.pressure_mmhg)
        instance.date_time = validated_data.get('date_time', instance.date_time)
        instance.save()
            
        return instance