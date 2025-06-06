from django.db import models
from doctor.models import Doctor
from patient.models import Patient

# Create your models here.
#-------------------------

# [SENU]: fully written

class ReserveStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved' 
    COMPLETED = 'completed', 'Completed'
    CANCELLED =  'cancelled', 'Cancelled'
    OUTDATED = 'outdated', 'Outdated' 


class Days(models.TextChoices):
    SAT = 'sat', 'Saturday'
    SUN = 'sun', 'Sunday'
    MON = 'mon', 'Monday'
    TUE = 'tue', 'Tuesday' 
    WED = 'wed', 'Wednesday'
    THU = 'thu', 'Thursday'
    FRI = 'fri', 'Friday'




class Appointment(models.Model):

    # id is auto added
    # [FK]: one to many (doctor, patient)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')

    # reserve status: the reservation status for teh appointments
    reserve_status = models.CharField(max_length=15, choices=ReserveStatus.choices, default=ReserveStatus.PENDING)

    # specified day by the patient [from booking] and doctor [from scheduler]
    day = models.CharField(max_length=20, choices=Days.choices)

    # date and times [from-to]
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()

    # necessary texts
    reason_of_visit = models.TextField(max_length=200, blank=True) # from patient
    reason_of_cancellation = models.TextField(max_length=200, blank=True) # from doctor
    doctor_notes = models.TextField(max_length=200, blank=True) # from doctor







    