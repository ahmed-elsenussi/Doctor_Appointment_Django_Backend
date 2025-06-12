from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField



# [SENU] comments

class Days(models.TextChoices):
    SAT = 'sat', 'Saturday'
    SUN = 'sun', 'Sunday'
    MON = 'mon', 'Monday'
    TUE = 'tue', 'Tuesday' 
    WED = 'wed', 'Wednesday'
    THU = 'thu', 'Thursday'
    FRI = 'fri', 'Friday'


# [SENU]: SPECIALIZATION MODEL
class Specialization(models.Model):
    # id is auto added
    name  = models.CharField(max_length=200, unique=True, null=False) 




class Doctor(models.Model):

    # primary key and foreigin key for the user table
    doctor_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # specialization [element is fk in specialization model]
    # django automatically creates the intermediate (join) table behind the scenes for you.
    specializations = models.ManyToManyField(Specialization, related_name='doctors')

    # images
    doctor_image_path = models.ImageField(upload_to='doctors/images/', null=True, blank=True)
    national_id_image_path = models.ImageField(upload_to='doctors/national_ids/', null=True, blank=True)
    background_image_path = models.ImageField(upload_to='doctors/backgrounds/', null=True, blank=True)


    #  text
    doctor_bio = models.CharField(max_length=200 ,null=True, blank=True)
    location  = models.CharField(max_length=200 ,null=True, blank=True)

    # availbilities
    doctor_availability = models.BooleanField(default=False)
    available_days = ArrayField(models.CharField(max_length=3, choices=Days.choices), default=list, blank=True,null=True)

    # [AMS] override to return a string representation of the doctor
    def __str__(self):
        return f"Doctor: {self.doctor_id.name} - Specializations: {', '.join([spec.name for spec in self.specializations.all()])}"