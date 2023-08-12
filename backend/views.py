from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer

from .models import Responsible, Room, Profession, EnviromentalParameters
from .serializers import EnviromentalsParametersSerializer




@api_view(['GET'])
def getEnviromentalParameters(request):
    parameters = EnviromentalParameters.objects.all()
    serializer = EnviromentalsParametersSerializer(parameters, many=True)
    
    return Response(serializer.data)

