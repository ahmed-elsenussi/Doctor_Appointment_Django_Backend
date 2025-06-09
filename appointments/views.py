from rest_framework import viewsets, status
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend # [SENU]:for effcient filterting
from .filters import AppointmentFilter #[SENU]: custom filter made to filter 'NOT EQUAL'

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




# -----INTERPRETATION---------------------------------------------------
# [SENU]: COMMON HEADER
# <Location>:     URL of the newly created resource
# <Content-Type>: The media type of the returned content.

