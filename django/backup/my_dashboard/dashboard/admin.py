from django.contrib import admin
from .models import Metric
from .models import Student, AttendanceRecord


admin.site.register(Metric)





admin.site.register(Student)
admin.site.register(AttendanceRecord)

