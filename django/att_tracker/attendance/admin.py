from django.contrib import admin
from .models import Student, Session, Attendance

admin.site.register(Student)
admin.site.register(Session)
admin.site.register(Attendance)

