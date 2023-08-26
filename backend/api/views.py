from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import *
from backend.models import *


from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from backend.models import Responsible, Room, Profession, EnviromentalParameters
from .serializers import EnvironmentalParametersSerializer, RoomSelectSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEnviromentalParameters(request):
    user = request.user
    parameters = EnviromentalParameters.objects.all()
    serializer = EnvironmentalParametersSerializer(parameters, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])

def getEnviromentalParameter(request, pk):
    parameters = EnviromentalParameters.objects.get(id=pk)
    serializer = EnvironmentalParametersSerializer(parameters, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSelectSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createEnvironmentalParameters(request):
    serializer = EnvironmentalParametersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def updateEnvironmentalParameters(request, pk):
    try:
        environmental_params = EnviromentalParameters.objects.get(pk=pk)
    except EnviromentalParameters.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EnvironmentalParametersSerializer(instance=environmental_params, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteEnvironmentalParameters(request, pk):
    try:
        environmental_params = EnviromentalParameters.objects.get(pk=pk)
    except EnviromentalParameters.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    environmental_params.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)