from django.db import models
from user.models import CustomUser
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Course(models.Model):
    course_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name
    
class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=50)
    total_marks = models.PositiveIntegerField()
    total_question_number = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(default=60)  # Duration of the exam in minutes
    end_time = models.DateTimeField(null=True, blank=True)  # Time when the exam ends

    def __str__(self):
        return self.exam_name
    
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is being created
            self.end_time = timezone.now() + timezone.timedelta(minutes=self.duration_minutes)
        super().save(*args, **kwargs)

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=400)
    content = models.TextField(blank=True, null=True)
    mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=300, blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class Result(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s result for {self.exam.exam_name}"
    
class Answer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer for {self.question.question_text} by {self.student.username}"
    
@receiver(pre_save, sender=Exam)
def update_exam_end_time(sender, instance, **kwargs):
    if instance.pk:  # If the instance is being updated
        return  # Don't update end time if already set
    instance.end_time = timezone.now() + timezone.timedelta(minutes=instance.duration_minutes)