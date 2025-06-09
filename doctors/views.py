# written by [SENU]
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Doctor, Specialization
from .serializers import DoctorSerializer, SpecializationSerializer


# VIEWSET FOR THE DOCTOR
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get', 'put'], url_path='me')
    def me(self, request):
        try:
            # Assuming `doctor_id` is a OneToOneField to User
            doctor = Doctor.objects.get(doctor_id=request.user)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor profile not found.'}, status=404)

        if request.method == 'GET':
            serializer = self.get_serializer(doctor)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = self.get_serializer(doctor, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data) 

# VIEWSET FOR THE SPECIALIZATION
class SpecializatoinViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer