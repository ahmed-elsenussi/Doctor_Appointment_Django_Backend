from rest_framework import serializers
from .models import Appointment
from patients.models import Patient
from patients.serializers import PatientSerializer

# [SENU]: to validate and make the communication between the client and the backend
class AppointmentSerializer(serializers.ModelSerializer):

    # to also fetch the patient data [OLD IS GOLD]
    # patient_id = PatientSerializer(read_only=True)

    # PID , PATIENT
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        required=False,
        allow_null=True
    )
    patient = PatientSerializer(source='patient_id', read_only=True)


    class Meta:
        model = Appointment
        fields=  '__all__'