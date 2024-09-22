from django.db import models

class Metric(models.Model):
    name = models.CharField(max_length=200)
    value = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f'{self.student.name} - {self.date} - {self.status}'

import random

class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('Exercise', 'Exercise'),
        ('Assignment', 'Assignment'),
        ('Assessment', 'Assessment'),
        ('Project', 'Project'),
    ]

    name = models.CharField(max_length=200)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    student = models.CharField(max_length=100)  # Replace with ForeignKey if linked to students
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.task.name}"
