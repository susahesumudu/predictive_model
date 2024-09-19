from django.db import models
from django.utils import timezone
from datetime import timedelta


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Session(models.Model):
    date = models.DateField(default=timezone.now)
    session_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.session_name} on {self.date}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('L', 'Late'),
        ('A', 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.status} for {self.session.session_name}"




from django.db import models
from django.utils import timezone
from datetime import timedelta

class ScheduledSession(models.Model):
    SESSION_FREQUENCY_CHOICES = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
    ]
    session_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    frequency = models.CharField(max_length=1, choices=SESSION_FREQUENCY_CHOICES, default='W')
    repeat_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.session_name} on {self.start_time}"

    def is_recurring(self):
        return self.frequency is not None and self.repeat_until is not None

# Auto-Creation Function to generate sessions based on recurrence
def create_recurring_sessions():
    sessions = ScheduledSession.objects.filter(repeat_until__gte=timezone.now().date())

    for session in sessions:
        next_session_date = session.start_time
        while next_session_date.date() <= session.repeat_until:
            if session.frequency == 'D':
                next_session_date += timedelta(days=1)
            elif session.frequency == 'W':
                next_session_date += timedelta(weeks=1)
            elif session.frequency == 'M':
                next_session_date += timedelta(weeks=4)

            # Check if session already exists to avoid duplicates
            if not ScheduledSession.objects.filter(start_time=next_session_date).exists():
                ScheduledSession.objects.create(
                    session_name=session.session_name,
                    start_time=next_session_date,
                    end_time=next_session_date + (session.end_time - session.start_time),
                    frequency=session.frequency,
                    repeat_until=session.repeat_until
                )

