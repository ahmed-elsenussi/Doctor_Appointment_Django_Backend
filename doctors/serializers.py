from rest_framework import serializers
from .models import Doctor, Specialization

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

    class Meta:
        model = Doctor
        fields = [
            'doctor_id',
            'specializations',        # read nested specialization
            'specialization_ids',     # write with just ids
            'doctor_image_path',
            'available_days',         #[OKS] for doctor availability      
            'doctor_availability',     #[OKS] for doctor availability
            'national_id_image_path',
            'background_image_path',
            'doctor_bio',
            'location',
        ]
