from django.contrib import admin
from datetime import timedelta  # Import timedelta for date manipulation

from .models import (
    Course, Module, Task, Activity, Teacher, Student, Demo, Batch,
    Session, LessonPlan, TrainingPlan, CoursePlan, StudentSubmission, StudentProgress,
)
import random
from django.utils.timezone import now

# Custom action to generate activities
def generate_activities(modeladmin, request, queryset):
    activity_types = [
        "exercise", "work_project", "assignment", "assessment",
        "discussion", "lecture", "demonstration", "workshop",
    ]
    session_types = ["theory", "practical"]

    for task in queryset:
        for i in range(10):  # Generate 10 activities per task
            Activity.objects.create(
                task=task,
                title=f"{task.title} Activity {i + 1}",
                activity_type=random.choice(activity_types),
                session_type=random.choice(session_types),
                duration_hours=round(random.uniform(1, 4), 1)  # Random duration between 1 to 4 hours
            )

    modeladmin.message_user(request, "Activities created for selected tasks")

generate_activities.short_description = "Generate 10 activities for each selected task"

# Register the Task model with the custom action





# Custom action to generate course plans
def generate_course_plan(modeladmin, request, queryset):
    for course in queryset:
        # Create a course plan for the selected course
        course_plan = CoursePlan.objects.create(
            course=course,
            published_by=request.user,
            start_date=now().date(),
            end_date=now().date() + timedelta(days=180)  # Example: 6 months from now
        )
        # Add modules to the course plan
        modules = Module.objects.filter(course=course)
        course_plan.modules.set(modules)
        course_plan.save()

    modeladmin.message_user(request, "Course plans created for selected courses")

generate_course_plan.short_description = "Generate course plans for selected courses"


def generate_training_plan(modeladmin, request, queryset):
    for batch in queryset:
        # Create a training plan for the selected batch
        training_plan = TrainingPlan.objects.create(
            batch=batch,
            weeks=12,  # Example: 12-week training plan
            months=3   # Example: 3 months of training
        )
        # Add tasks to the training plan (all tasks related to the batch's course)
        tasks = Task.objects.filter(module__course=batch.course)
        training_plan.tasks.set(tasks)
        training_plan.save()

    modeladmin.message_user(request, "Training plans created for selected batches")

generate_training_plan.short_description = "Generate training plans for selected batches"



def generate_lesson_plan(modeladmin, request, queryset):
    for batch in queryset:
        # Create a lesson plan for the selected batch
        lesson_plan = LessonPlan.objects.create(
            batch=batch,
            published_by=request.user,
            day=now().date()  # The day the lesson plan is created
        )
        # Add tasks and sessions to the lesson plan (from the batch's course)
        tasks = Task.objects.filter(module__course=batch.course)
        sessions = Session.objects.filter(batch=batch)
        lesson_plan.tasks.set(tasks)
        lesson_plan.sessions.set(sessions)
        lesson_plan.save()

    modeladmin.message_user(request, "Lesson plans created for selected batches")

generate_lesson_plan.short_description = "Generate lesson plans for selected batches"



# Custom action to generate sessions for a batch
def generate_sessions(modeladmin, request, queryset):
    for batch in queryset:
        # Example: Generate sessions over a 4-week period, with 2 sessions per week
        start_date = now().date()
        session_count = 1

        # Fetch tasks related to the batch's course to create sessions based on the course tasks
        tasks = Task.objects.filter(module__course=batch.course)

        for week in range(4):  # Example: Over 4 weeks
            for day in range(2):  # Example: 2 sessions per week
                session_date = start_date + timedelta(weeks=week, days=day * 3)  # Spread the sessions
                session_title = f"Session {session_count}: {tasks[week % len(tasks)].title}"
                
                # Create session
                session = Session.objects.create(
                    batch=batch,
                    title=session_title,
                    session_type="theory" if session_count % 2 == 0 else "practical",
                    date=session_date
                )

                # Optionally, associate the activities related to the tasks
                activities = Activity.objects.filter(task=tasks[week % len(tasks)])
                session.activities.set(activities)
                
                session_count += 1

    modeladmin.message_user(request, "Sessions created for selected batches.")

generate_sessions.short_description = "Generate sessions for selected batches"


# Customize admin interface for related models
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1

class StudentInline(admin.TabularInline):
    model = Batch.students.through  # ManyToMany relation through Batch
    extra = 1

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1

# Admin for Course with inline for Modules
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [ModuleInline]
    actions = [generate_course_plan]  # Register the action

# Admin for Module with inline for Tasks
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title',)
    list_filter = ('course',)
    inlines = [TaskInline]

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1  # Number of extra empty activity forms to display in the admin

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'description')
    search_fields = ('title', 'module__title')  # Enable search by task and module
    list_filter = ('module',)  # Add filter by module in the admin sidebar
    
    inlines = [ActivityInline]  # Display related activities inline with tasks
    actions = [generate_activities]  # Register the custom action



@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'activity_type', 'session_type', 'duration_hours')
    search_fields = ('title', 'activity_type')
    list_filter = ('task', 'activity_type', 'session_type')

# Admin for Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise')
    search_fields = ('user__username', 'expertise')

# Admin for Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrolled_date')
    search_fields = ('user__username',)
    list_filter = ('enrolled_date',)

# Admin for Demo
@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    list_display = ('title', 'demo_date')
    search_fields = ('title',)
    list_filter = ('demo_date',)

# Admin for Batch with inline for Sessions and Students
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'teacher', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('course', 'teacher', 'start_date', 'end_date')
    inlines = [SessionInline, StudentInline]
    actions = [generate_training_plan, generate_lesson_plan,generate_sessions]  # Now has both 

# Admin for Session
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'batch', 'session_type', 'date')
    search_fields = ('title',)
    list_filter = ('batch', 'session_type', 'date')


# Admin for Training Plan
@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ('batch', 'weeks', 'months')
    search_fields = ('batch__name',)
    filter_horizontal = ('tasks',)  # For ManyToMany fields

@admin.register(CoursePlan)
class CoursePlanAdmin(admin.ModelAdmin):
    list_display = ('course', 'published_by', 'published_date', 'start_date', 'end_date')
    list_filter = ('course', 'published_date', 'start_date', 'end_date')
    search_fields = ('course__name', 'published_by__username')

@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('batch', 'published_by', 'published_date', 'day')
    list_filter = ('batch', 'published_date', 'day')
    search_fields = ('batch__name', 'published_by__username')
    filter_horizontal = ('tasks', 'sessions')

@admin.register(StudentSubmission)
class StudentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'task', 'activity', 'submission_date')
    list_filter = ('student', 'submission_date')
    search_fields = ('student__user__username',)

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'total_exercises', 'total_activities')
    search_fields = ('student__user__username',)
