from django.db import models
from doctors.models import Doctor
from patients.models import Patient

# [SENU] comments
#-------------------------


class ReserveStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
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
    # <FK> one to many (doctor, patient)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', blank=True, null=True)

    # reserve status: the reservation status for teh appointments
    reserve_status = models.CharField(max_length=15, choices=ReserveStatus.choices, default=ReserveStatus.AVAILABLE)

    # specified day by the patient [from booking] and doctor [from scheduler]
    day = models.CharField(max_length=20, choices=Days.choices)

    # date and times [from-to]
    date = models.DateField(blank=True, null=True) #[SENU]: I made the date optional for now
    from_time = models.TimeField()
    to_time = models.TimeField()

    # necessary texts
    reason_of_visit = models.TextField(max_length=200, blank=True) # from patient
    reason_of_cancellation = models.TextField(max_length=200, blank=True) # from doctor
    doctor_notes = models.TextField(max_length=200, blank=True) # from doctor







    