from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# [SENU] comments
# ----------------
# NOTE: NEW USER BASED ON EMAIL
# CUSTOM MANAGER: MADE FOR THIS
# PASSWORD: REMOVED BECAUSE EXIST ALREADY
#========================================


# roles
class RoleChoices(models.TextChoices):
    GUEST = 'guest', 'Guest'
    ADMIN = 'admin', 'Admin'
    DOCTOR = 'doctor', 'Doctor'
    PATIENT = 'patient', 'Patient'


# OVERRIDE DEFAULT USER CREATION LOGIC
class CustomUserManager(BaseUserManager):

    # TELLING DJANOG HOW TO CREATE THE USER
    def create_user(self, email, password=None, **extra_fields):
        #  email instead of username
        if not email:
            raise ValueError("Users must have an email address")
        #  convert to consistent format 
        email = self.normalize_email(email)
        # create the model
        user = self.model(email=email, **extra_fields)
        # add the password sent + save
        user.set_password(password)
        user.save()
        return user


    # TELLING DJANGO HOW TO CREATE THE SUPER USER [ADMIN] 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)





# =========CREATING THE USER MODEL============
class User(AbstractBaseUser, PermissionsMixin):

    # id already auto added
    name = models.CharField(max_length=200)  # name, not unique
    email = models.EmailField(max_length=200, unique=True)  # used as username [for django system, her is the unique one]
    email_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.GUEST)
    is_approved = models.BooleanField(default=False)

    # this is for django admin and auth
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # tells django to use our custom manager
    objects = CustomUserManager()

    # login field configuration:
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


    # in case printing the user
    def __str__(self):
        return self.name
