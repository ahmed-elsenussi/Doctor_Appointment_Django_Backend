from rest_framework import serializers
from .models import Doctor, Specialization
from appointments.models import Appointment

# SPECIALIZATION SERIALIZER
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

# DOCTOR SERIALIZER
class DoctorSerializer(serializers.ModelSerializer):

    # Show specializations as nested objects in GET
    specializations = SpecializationSerializer(many=True, read_only=True)

    # Accept specialization IDs for write (POST/PUT)
    specialization_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Specialization.objects.all(),
        write_only=True,
        source='specializations'
    )

    # Custom field to check if the doctor has at least one available appointment
    has_available_appointment = serializers.SerializerMethodField()

    # Custom field to fetch the doctor's name
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'doctor_id',
            'doctor_name',            # Add the doctor's name
            'specializations',        # read nested specialization
            'specialization_ids',     # write with just ids
            'doctor_image_path',
            'available_days',         # [OKS] for doctor availability      
            'doctor_availability',    # [OKS] for doctor availability
            'national_id_image_path',
            'background_image_path',
            'doctor_bio',
            'location',
            'has_available_appointment',  # Add the custom field
        ]

    # Ensure this method is properly indented and inside the class
    def get_has_available_appointment(self, obj):
        # Use the Doctor instance (obj) directly for filtering
        return Appointment.objects.filter(doctor_id=obj, reserve_status='available').exists()

    # Method to fetch the doctor's name
    def get_doctor_name(self, obj):
        # Access the related User model to get the first and last name
        return obj.doctor_id.name 