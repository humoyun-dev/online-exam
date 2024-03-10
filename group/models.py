from django.db import models
from exam.models import Course
from user.models import CustomUser

class Groups(models.Model):
    group_name = models.CharField(max_length=150)
    teacher = models.CharField(max_length=150)
    exams = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ManyToManyField(CustomUser, related_name='students')

    class Meta:
        verbose_name_plural = "Groups"
    def __str__(self):
        return self.group_name