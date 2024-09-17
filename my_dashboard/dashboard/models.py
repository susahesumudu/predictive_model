from django.db import models
import random

# Represents different metrics (unrelated to course structure)
class Metric(models.Model):
    name = models.CharField(max_length=200)
    value = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Batch model for grouping students
class Batch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Represents a module in the course, which contains exercises, assignments, and assessments
class Module(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


# Task model represents exercises, assignments, assessments, and projects
class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('Exercise', 'Exercise'),
        ('Assignment', 'Assignment'),
        ('Assessment', 'Assessment'),
        ('Project', 'Project'),
    ]

    name = models.CharField(max_length=200)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)  # Link each task to a module

    def __str__(self):
        return f"{self.module.name} - {self.name} ({self.task_type})"


# Represents students enrolled in the course and assigned to a batch
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# A schedule entry where each student is assigned tasks (exercises, assignments, etc.)
class Schedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.task.name} on {self.date_assigned}"


# Attendance tracking for students
class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f'{self.student.name} - {self.date} - {self.status}'


# Projects that span multiple modules in the course
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    modules = models.ManyToManyField(Module, related_name='projects')

    def __str__(self):
        return self.name

