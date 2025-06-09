from django_filters import rest_framework as filters
from .models import Appointment

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class AppointmentFilter(filters.FilterSet):
    # [SENU]: exclude multiple values
    not_reserve_status = CharInFilter(field_name='reserve_status', exclude=True)

    class Meta:
        model = Appointment
        fields = ['reserve_status', 'not_reserve_status']
