from django.db import models
from users.models import User


# [SENU] comments
class Patient(models.Model):

    # primary key and foreigin key for the user table
    patient_id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    patient_image_path = models.ImageField(upload_to='patient_images/')
    phone = models.CharField(max_length=17, null=True, blank=True)  # Optional phone number
    date_of_birth = models.DateField(null=True, blank=True)  # Optional date of birth
    
    def __str__(self):
        return f"{self.patient_id.name}"

