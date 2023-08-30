from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from backend.models import Responsible, Room, EnviromentalParameters
from .serializers import EnvironmentalParametersSerializer, RoomSelectSerializer, ResponsibleSerializer

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
@permission_classes([IsAuthenticated])
def getEnviromentalParameter(request, pk):
    parameters = EnviromentalParameters.objects.get(id=pk)
    serializer = EnvironmentalParametersSerializer(parameters, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSelectSerializer(rooms, many=True)
    return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def createEnvironmentalParameters(request):
#     serializer = EnvironmentalParametersSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     print(serializer.errors)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def createEnvironmentalParameters(request):
#     serializer = EnvironmentalParametersSerializer(data=request.data)
#     if serializer.is_valid():
#         # Добавляем валидное поле "responsible"
#         serializer.validated_data['responsible'] = request.user.responsible.id
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createEnvironmentalParameters(request):
    serializer = EnvironmentalParametersSerializer(data=request.data)

    if serializer.is_valid():
        room_data = request.data.get('room')
        responsible_data = request.data.get('responsible')

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
            temperature_celsius=serializer.validated_data['temperature_celsius'],
            humidity_percentage=serializer.validated_data['humidity_percentage'],
            pressure_kpa=serializer.validated_data['pressure_kpa'],
            pressure_mmhg=serializer.validated_data['pressure_mmhg'],
            date_time=serializer.validated_data['date_time']
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def deleteEnvironmentalParameters(request, pk):
    try:
        environmental_params = EnviromentalParameters.objects.get(pk=pk)
    except EnviromentalParameters.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    environmental_params.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    if user.is_authenticated:
        try:
            responsible = Responsible.objects.get(user=user)
            serializer = ResponsibleSerializer(responsible)
            return Response(serializer.data)
        except Responsible.DoesNotExist:
            return Response({'error': 'Responsible not found'}, status=404)
    else:
        return Response({'error': 'User not authenticated'}, status=401)