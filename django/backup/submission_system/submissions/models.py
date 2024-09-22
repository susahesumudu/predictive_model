from django.db import models
from django.utils import timezone

# Task model
TASK_TYPE_CHOICES = [
    ('Exercise', 'Exercise'),
    ('Assignment', 'Assignment'),
    ('Assessment', 'Assessment'),
    ('Project', 'Project'),
]

class Task(models.Model):
    title = models.CharField(max_length=200)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='Exercise')
    description = models.TextField()
    submission_deadline = models.DateTimeField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.task_type})"

# Exercise model
class Exercise(models.Model):
    student_name = models.CharField(max_length=100)
    exercise_title = models.CharField(max_length=100)
    submission_time = models.DateTimeField()
    completed_on_time = models.CharField(max_length=20)
    level_of_completion = models.CharField(max_length=20)
    quality_of_work = models.IntegerField()
    learning_outcome = models.TextField()
    challenges = models.TextField(null=True, blank=True)
    teacher_feedback = models.TextField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student_name} - {self.exercise_title}"

