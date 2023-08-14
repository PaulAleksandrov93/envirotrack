from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from rest_framework import status

from .models import Responsible, Room, Profession, EnviromentalParameters
from .serializers import EnvironmentalParametersSerializer


def getRoutes(request):
    routes = [
        '/backend/token',
        '/backend/token/refresh'
    ]
    return Response(routes, safe=False)



@api_view(['GET'])
def getEnviromentalParameters(request):
    parameters = EnviromentalParameters.objects.all()
    serializer = EnvironmentalParametersSerializer(parameters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getEnviromentalParameter(request, pk):
    parameters = EnviromentalParameters.objects.get(id=pk)
    serializer = EnvironmentalParametersSerializer(parameters, many=False)
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