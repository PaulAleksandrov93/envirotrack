from django.db import models
from django.contrib.auth.models import User


class Profession(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Responsible(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True)
    # rooms_responsible_for = models.ManyToManyField(Room, related_name="responsibles")

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'


class Room(models.Model):
    room_number = models.CharField(max_length=10)
    responsible_persons = models.ManyToManyField(Responsible, related_name="rooms")

    def __str__(self):
        return f'Помещение № {self.room_number}'


class MeasurementInstrument(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=50)
    calibration_date = models.DateField()
    calibration_interval = models.PositiveIntegerField()  # Интервал в месяцах, например

    def __str__(self):
        return self.name
    

class EnviromentalParameters(models.Model):
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2)
    humidity_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    pressure_kpa = models.DecimalField(max_digits=7, decimal_places=2)
    pressure_mmhg = models.DecimalField(max_digits=7, decimal_places=2)
    date_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    responsible = models.ForeignKey(Responsible, related_name='environmental_parameters', on_delete=models.SET_NULL, null=True)
    measurement_instrument = models.ForeignKey(MeasurementInstrument, on_delete=models.CASCADE, null=True) 

    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Дата и время создания
    created_by = models.ForeignKey(User, related_name='created_parameters', on_delete=models.SET_NULL, null=True)  # Кто создал
    modified_at = models.DateTimeField(auto_now=True, null=True)  # Дата и время последнего изменения
    modified_by = models.ForeignKey(User, related_name='modified_parameters', on_delete=models.SET_NULL, null=True)  # Кто изменил

    def __str__(self):
        return f'{self.room.room_number} - {self.date_time}'

