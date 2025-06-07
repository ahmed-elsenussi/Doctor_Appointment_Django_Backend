from django.db import models
from users.models import User


# [SENU] comments
class Patient(models.Model):

    # primary key and foreigin key for the user table
    patient_id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    patient_image_path = models.ImageField(upload_to='patient_images/')
    phone = models.CharField(max_length=17)
    date_of_birth = models.DateField()

