from rest_framework import serializers
from .models import Appointment

# [SENU]: to validate and make the communication between the client and the backend
class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields=  '__all__'