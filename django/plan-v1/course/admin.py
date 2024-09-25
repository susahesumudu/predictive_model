# admin.py
from django.contrib import admin
from .models import Course, Module, Task, Activity



# Register the Course model to make it visible in the admin panel
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'duration')  # Fields to display in the list view
    search_fields = ('title',)  # Enable search by course title


admin.site.register(Module)
admin.site.register(Task)
admin.site.register(Activity)

