from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

class Course(models.Model):
    name = models.CharField(max_length=255)  # Course name (e.g., "Computer Science")
    description = models.TextField()  # Optional course description
    duration = models.IntegerField(help_text="Duration in weeks")  # Duration of the course in weeks

    def __str__(self):
        return self.name



TASK_TYPE_CHOICES = [
    ('Exercise', 'Exercise'),
    ('Assignment', 'Assignment'),
    ('Assessment', 'Assessment'),
    ('Project', 'Project'),
]

COMPLETION_STATUS_CHOICES = [
    ('On Time', 'On Time'),
    ('Late', 'Late'),
]

REVIEW_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Reviewed', 'Reviewed'),
]



class Batch(models.Model):
    name = models.CharField(max_length=100)  # Batch name
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Teacher'})  # Assign Teacher to Batch
    students = models.ManyToManyField(User, related_name="student_batches", limit_choices_to={'groups__name': 'Student'})  # Multiple students in a batch
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Add ForeignKey to Course
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name



class Task(models.Model):
    title = models.CharField(max_length=255)
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)  # Exercise, Assignment, Project
    description = models.TextField()
    submission_deadline = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Teacher who created the task
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)  # Assign Task to Batch

    def __str__(self):
        return self.title


class Exercise(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises")
    exercise_title = models.CharField(max_length=100)
    submission_time = models.DateTimeField()
    completed_on_time = models.CharField(max_length=20, choices=COMPLETION_STATUS_CHOICES)
    level_of_completion = models.CharField(max_length=20)
    quality_of_work = models.IntegerField()
    learning_outcome = models.TextField()
    challenges = models.TextField(null=True, blank=True)
    teacher_feedback = models.TextField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES, default='Pending')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.username} - {self.exercise_title}"


class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Student'})
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s submission for {self.task.title}"



class TaskModelTest(TestCase):
    def setUp(self):
        Task.objects.create(title="Test Task", task_type="Exercise", description="Test description", submission_deadline="2024-09-20")

    def test_task_creation(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(task.task_type, "Exercise")

class SubmitExerciseViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password')
        self.client.login(username='teststudent', password='password')
        self.task = Task.objects.create(title="Test Task", task_type="Exercise", description="Test description", submission_deadline="2024-09-20")

    def test_submit_exercise(self):
        response = self.client.post(reverse('submit_exercise'), {
            'task_id': self.task.id,
            'level_of_completion': 'Complete',
            'quality_of_work': 8,
            'learning_outcome': 'Good learning',
            'challenges': 'None',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
