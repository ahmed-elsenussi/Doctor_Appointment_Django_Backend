from django_filters import rest_framework as filters
from .models import Appointment

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class AppointmentFilter(filters.FilterSet):
    # [SENU]: exclude multiple values
    not_reserve_status = CharInFilter(field_name='reserve_status', exclude=True)
    doctor_id = filters.NumberFilter(field_name='doctor_id')
    is_deleted = filters.BooleanFilter(field_name='is_deleted')  # Add filter for is_deleted

    class Meta:
        model = Appointment
        fields = ['reserve_status', 'not_reserve_status', 'doctor_id', 'is_deleted']
