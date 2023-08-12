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


class EnviromentalsParametersSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    class Meta:
        model = EnviromentalParameters
        fields = '__all__'