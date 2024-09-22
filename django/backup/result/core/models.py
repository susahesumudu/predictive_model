from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rfid_tag = models.CharField(max_length=255, unique=True)
    attendance_percentage = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    class Meta:
        db_table = 'student'

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Activity(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    class Meta:
        db_table = 'attendance'

class Prediction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    predicted_pass = models.BooleanField(default=False)
    feedback = models.TextField(null=True, blank=True)

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rubric = models.JSONField()  # Store rubric criteria
    class Meta:
        db_table = 'task'

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    #graded = models.BooleanField(default=False)
    marks = models.FloatField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'submission'


