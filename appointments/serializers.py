from rest_framework import serializers
from .models import Appointment
from patients.models import Patient
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer

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

  #[OKS] display the doctor's name in the appointment serializer
    doctor_name = DoctorSerializer(source='doctor_id', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient_id',
            'patient',
            'doctor_id',
            'doctor_name',  
            'reserve_status',
            'day',
            'date',
            'from_time',
            'to_time',
            'reason_of_visit',
            'reason_of_cancellation',
            'doctor_notes',
        ]