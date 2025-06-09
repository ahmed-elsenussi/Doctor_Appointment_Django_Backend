# writen by [SENU]
from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    """ 
    @author: SENU
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer