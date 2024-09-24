from django.db import models
from django.contrib.auth.models import User

class AttendanceRecord(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.username} - {self.check_in_time}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rfid_tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.user.username

