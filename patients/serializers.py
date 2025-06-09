# written by [SENU]
from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):

    # [SENU]: MIRROR NAME FROM USER TABLE
    name = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['patient_id', 'name', 'patient_image_path', 'phone', 'date_of_birth']

    # IMPORTANT
    def get_name(self, obj):
        return obj.patient_id.name

