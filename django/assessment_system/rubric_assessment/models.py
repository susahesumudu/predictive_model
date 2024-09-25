# models.py

from django.db import models
from django.utils import timezone

class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Rubric(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Criteria(models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_points = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.rubric.name})"

class Activity(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)  # Link activity to a rubric
    name = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)

    def mark_completed(self):
        self.completed = True
        self.date_completed = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.name} - {self.student.name}"

class Assessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    total_score = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.rubric.name}"

