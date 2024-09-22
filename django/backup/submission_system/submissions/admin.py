from django.contrib import admin

# Register your models here.

from .models import Task, Exercise
admin.site.register(Task)
admin.site.register(Exercise)

