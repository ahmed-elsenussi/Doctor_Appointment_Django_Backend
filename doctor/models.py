from django.db import models
from user.models import User
from django.contrib.postgres.fields import ArrayField



# [SENU]: fully written

class Days(models.TextChoices):
    SAT = 'sat', 'Saturday'
    SUN = 'sun', 'Sunday'
    MON = 'mon', 'Monday'
    TUE = 'tue', 'Tuesday' 
    WED = 'wed', 'Wednesday'
    THU = 'thu', 'Thursday'
    FRI = 'fri', 'Friday'


# SPECIALIZATION MODEL
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
    doctor_image_path = models.ImageField(upload_to='doctor/images/')
    national_id_image_path = models.ImageField(upload_to='doctor/national_ids/')
    background_image_path = models.ImageField(upload_to='doctor/backgrounds/')


    #  text
    doctor_bio = models.CharField(max_length=200)
    location  = models.CharField(max_length=200)

    # availbilities
    doctor_availability = models.BooleanField(default=False)
    available_days = ArrayField(models.CharField(max_length=3, choices=Days.choices), default=list, blank=True)
