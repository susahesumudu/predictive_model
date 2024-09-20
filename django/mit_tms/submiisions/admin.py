from django.contrib import admin
from .models import Task, Exercise, Batch, Course



# Register the Course model in the admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'duration']
    search_fields = ['name']  # Ensure the 'name' field of Course is searchable

# Register the Batch model in the admin
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'course', 'start_date', 'end_date']
    search_fields = ['name', 'course__name', 'teacher__username']  # Define search fields for Batch
    list_filter = ['course', 'teacher']
    fields = ['name', 'teacher', 'students', 'course', 'start_date', 'end_date']
    filter_horizontal = ['students']  # Make it easier to select multiple students
    autocomplete_fields = ['course']  # Use autocomplete for selecting courses

admin.site.register(Task)
admin.site.register(Exercise)


