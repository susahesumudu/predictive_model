from django.db import models
from django.contrib.auth.models import User  # Assuming User model is used for both students and teachers.

# Course, Modules, and Tasks
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.title} ({self.course.name})"

class Task(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.title} ({self.module.title})"

# Constants for activity types and session types
ACTIVITY_TYPE_CHOICES = [
    ('exercise', 'Exercise'),
    ('work_project', 'Work Project'),
    ('assignment', 'Assignment'),
    ('assessment', 'Assessment'),
    ('discussion', 'Discussion'),
    ('lecture', 'Lecture'),
    ('demonstration', 'Demonstration'),
    ('workshop', 'Workshop'),
]

SESSION_TYPE_CHOICES = [
    ('theory', 'Theory'),
    ('practical', 'Practical'),
]

class Activity(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    
    # New fields for activity type and session type
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    session_type = models.CharField(max_length=50, choices=SESSION_TYPE_CHOICES)
    
    # Duration of the activity in hours (e.g., 2 hours, 3 hours)
    duration_hours = models.DecimalField(max_digits=4, decimal_places=2)  # Allows for fractional hours (e.g., 1.5 hrs)
    
    def __str__(self):
        return f"{self.title} ({self.activity_type}, {self.session_type}, {self.duration_hours} hrs)"


# Batches, Sessions, and Students
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Demo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    demo_date = models.DateTimeField()
    
    def __str__(self):
        return self.title

class Batch(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, related_name='batches')
    demo = models.ForeignKey(Demo, on_delete=models.CASCADE, related_name='batches')  # One demo
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='batches')  # One teacher
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"Batch {self.name} - {self.course.name}"

class Session(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sessions')  # Sessions belong to a batch
    title = models.CharField(max_length=255)
    session_type = models.CharField(max_length=50)  # e.g. Demo, Regular
    activities = models.ManyToManyField(Activity, related_name='sessions')
    date = models.DateTimeField()
    
    def __str__(self):
        return f"Session {self.title} ({self.batch.name})"



class TrainingPlan(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='training_plans')
    weeks = models.IntegerField()
    months = models.IntegerField()
    tasks = models.ManyToManyField(Task, related_name='training_plans')

    def __str__(self):
        return f"Training Plan for Batch {self.batch.name}"



# Staff publishes the Course Plan
class CoursePlan(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_plans')
    modules = models.ManyToManyField('Module', related_name='course_plans')
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_course_plans')  # Staff user
    published_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Course Plan for {self.course.name} published by {self.published_by.username}"

# Teacher publishes the Lesson Plan with daily tasks and session schedules
class LessonPlan(models.Model):
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, related_name='lesson_plans')
    tasks = models.ManyToManyField('Task', related_name='lesson_plans')
    sessions = models.ManyToManyField('Session', related_name='lesson_plans')
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_lesson_plans')  # Teacher user
    published_date = models.DateTimeField(auto_now_add=True)
    day = models.DateField()  # Plan for each day

    def __str__(self):
        return f"Lesson Plan for Batch {self.batch.name} on {self.day}"

# Student Submission tracks the work done by students
class StudentSubmission(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='submissions')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/', null=True, blank=True)  # File submitted by student

    def __str__(self):
        return f"Submission by {self.student.user.username} for {self.task or self.activity}"

# Count the number of exercises or activities a student has completed
class StudentProgress(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='progress')
    total_exercises = models.IntegerField(default=0)  # Count of exercises done
    total_activities = models.IntegerField(default=0)  # Count of other activities

    def __str__(self):
        return f"{self.student.user.username} Progress"

    def update_progress(self):
        # Calculate the number of tasks/activities submitted by the student
        self.total_exercises = StudentSubmission.objects.filter(student=self.student, task__isnull=False).count()
        self.total_activities = StudentSubmission.objects.filter(student=self.student, activity__isnull=False).count()
        self.save()


