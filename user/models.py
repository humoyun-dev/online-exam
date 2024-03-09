# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Students_group(models.Model):
    group_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Groups of students"
    def __str__(self):
        return self.group_name


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    parents_phone_number = models.CharField(max_length=15, blank=True, null=True)
    group_of_student = models.ForeignKey(Students_group, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.username
