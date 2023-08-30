from rest_framework import serializers
from .models import Responsible, Room, EnviromentalParameters, User


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class EnvironmentalParametersSerializer(serializers.ModelSerializer):
    room = RoomSelectSerializer()
    responsible = ResponsibleSerializer()
    class Meta:
        model = EnviromentalParameters
        fields = ['id', 'room', 'temperature_celsius', 'humidity_percentage', 'pressure_kpa', 'pressure_mmhg', 'date_time', 'responsible']

    def create(self, validated_data):
        room_data = validated_data.pop('room', None)
        responsible_data = validated_data.pop('responsible', None)
        
        room = None
        if room_data:
            room, created = Room.objects.get_or_create(room_number=room_data.get('room_number'))

        responsible = None
        if responsible_data:
            responsible, created = Responsible.objects.get_or_create(
                first_name=responsible_data.get('first_name'),
                last_name=responsible_data.get('last_name'),
                patronymic=responsible_data.get('patronymic')
            )

        instance = EnviromentalParameters.objects.create(
            room=room,
            responsible=responsible,
            **validated_data
        )
        return instance