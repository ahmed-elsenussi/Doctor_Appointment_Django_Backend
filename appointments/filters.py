from .models import Appointment
from django_filters import rest_framework as filters

class AppointmentFilter(filters.FilterSet):

    # [SENU]: define that this filter is exclude
    not_reserve_status = filters.CharFilter(field_name = 'reserve_status', exclude = True)

    class Meta:
        model = Appointment
        fields = ['reserve_status', 'not_reserve_status']
