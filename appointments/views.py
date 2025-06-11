from rest_framework import viewsets, status
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend # [SENU]:for effcient filterting
from .filters import AppointmentFilter #[SENU]: custom filter made to filter 'NOT EQUAL'
from .utils import send_appointment_email # [AMS]-> 📧Send EMail to each of doctor and patient
from notifications.models import Notification
from django.urls import reverse
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# [SENU]: full CRUD for the appointment
#-----------------------------
    # Create appointment
    # Read all/one appointments
    # Update appointment
    # Delete appointment

class AppointmentViewSet(viewsets.ModelViewSet):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    # for effcient filteration
    filter_backends = [DjangoFilterBackend]
    filterset_class = AppointmentFilter #[SENU]: custom filter made to filter 'NOT EQUAL'


    # [SENU] override on the create to accept list of objects to be created
    def create(self, request, *args, **kwargs):
        
        # [THE MOST BRILLIANT STEP]
        is_many = isinstance(request.data, list)

        # use the same serializer we passed earlier
        serializer = self.get_serializer(data=request.data, many=is_many)

        # check validation as before
        serializer.is_valid(raise_exception=True)

        # createeeeeeeeeeeeeeeeeeeee
        self.perform_create(serializer)
        # generate 'Location' header for the newly created object
        locationHeader = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=locationHeader)
    
    
    # [AMS]-> 📧Send EMail to each of doctor and patient
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        previous_status = instance.reserve_status  # Save old status

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        new_status = serializer.instance.reserve_status

        # Send email only if reserve_status changed to "Pending"
        if previous_status != "Pending" and (new_status.lower() == "pending"):
            send_appointment_email(serializer.instance)

            # --- Notification logic ---
            appointment = serializer.instance
            doctor_user = appointment.doctor_id.doctor_id  # Doctor model -> User
            # Build appointment details
            details = (
                f"Patient: {appointment.patient_id.patient_id.name}\n"
                f"Day: {appointment.day}\n"
                f"Time: {appointment.from_time} - {appointment.to_time}\n"
                f"Reason: {appointment.reason_of_visit}\n"
                f"Status: {appointment.reserve_status}\n"
            )
            # Build a link to the appointment details (adjust the URL as per your frontend)
            appointment_link = f"http://localhost:3000/doctor/appointments/{appointment.id}"

            message = (
                f"You have a new appointment assigned!\n\n"
                f"{details}\n"
                f"View details: {appointment_link}"
            )

            Notification.objects.create(
                user=doctor_user,
                notification_type="reminder",
                message=message,
                data={
                    "appointment_id": appointment.id,
                    "link": appointment_link,
                }
            )

        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='my', permission_classes=[IsAuthenticated])
    def my_appointments(self, request):
        # Filter appointments where the patient user matches the logged-in user
        user = request.user
        appointments = Appointment.objects.filter(patient_id__patient_id=user)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    


# Inside AppointmentViewSet...
    @action(detail=True, methods=['post'], url_path='cancel', permission_classes=[IsAuthenticated])
    def cancel_appointment(self, request, pk=None):
        appointment = self.get_object()

        # Check if appointment is in 'Pending' status
        if appointment.reserve_status.lower() != 'pending':
            return Response(
                {"detail": "Only pending appointments can be canceled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if current user is the assigned patient
        if not appointment.patient_id or request.user != appointment.patient_id.patient_id:
            raise PermissionDenied("You are not allowed to cancel this appointment.")

        # Cancel the appointment
        appointment.patient_id = None
        appointment.reserve_status = "available"
        appointment.save()

        return Response({"detail": "Appointment canceled successfully."}, status=status.HTTP_200_OK)

# -----INTERPRETATION---------------------------------------------------
# [SENU]: COMMON HEADER
# <Location>:     URL of the newly created resource
# <Content-Type>: The media type of the returned content.

