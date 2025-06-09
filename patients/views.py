from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]  

    @action(detail=False, methods=['get', 'put'], url_path='me')
    def me(self, request):
        try:
            patient = Patient.objects.get(patient_id=request.user)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient profile not found.'}, status=404)

        if request.method == 'GET':
            serializer = self.get_serializer(patient)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = self.get_serializer(patient, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
