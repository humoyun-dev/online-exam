from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, **kwargs):
        raise NotImplementedError('Users must have a unique identifier.')

    def create_superuser(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set for superusers.')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(phone_number, password, **extra_fields)

    def _create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a user with the given phone number and password.
        """
        if not phone_number:
            raise ValueError('The phone number must be set.')

        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField(unique=True)
    parents_phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender_select = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    gender = models.CharField(choices=gender_select, max_length=6, null=True, blank=True)
    is_teacher = models.BooleanField(null=True)
    is_student = models.BooleanField(default=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)
