from django.db import models

# roles
class RoleChoices(models.TextChoices):
    GUEST = 'guest','Guest'
    ADMIN = 'admin','Admin'
    DOCTOR = 'doctor','Doctor'
    PATIENT = 'patient','Patient'



# Create your User models.
# ------------------------
class User(models.Model):

    # id already auto added
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    email_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.GUEST)
    is_approved = models.BooleanField(default=False)



#=============
from django.db import models

# roles
class RoleChoices(models.TextChoices):
    GUEST = 'guest', 'guest'
    ADMIN = 'admin', 'admin'
    DOCTOR = 'doctor', 'doctor'
    PATIENT = 'patient', 'patient'


# Create your User models.
# ------------------------
class User(models.Model):

    # id already auto added
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    email_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        default=RoleChoices.GUEST
    )
    is_approved = models.BooleanField(default=False)

#============