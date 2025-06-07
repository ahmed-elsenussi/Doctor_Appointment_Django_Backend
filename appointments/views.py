from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer


# [SENU]: full CRUD for the appointment
#-----------------------------
    # Create appointment
    # Read all/one appointments
    # Update appointment
    # Delete appointment

class AppointmentViewSet(viewsets.ModelViewSet):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer