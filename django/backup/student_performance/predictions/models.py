from django.db import models
from django.utils import timezone

class Student(models.Model):
    name = models.CharField(max_length=100)
    attendance_rate = models.FloatField()
    assignment_score = models.FloatField()
    exercise_completion = models.FloatField()
    engagement = models.FloatField()

    def __str__(self):
        return self.name

# Assignment model
class Assignment(models.Model):
    student = models.ForeignKey(Student, related_name='assignments', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    score = models.FloatField()
    is_completed = models.BooleanField(default=False)
    submission_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.student.name})"

