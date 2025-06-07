# written by [SENU]
from rest_framework import viewsets
from .models import Doctor, Specialization
from .serializers import DoctorSerializer, SpecializationSerializer


# VIEWSET FOR THE DOCTOR
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


# VIEWSET FOR THE SPECIALIZATION
class SpecializatoinViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer