from django.contrib import admin
from .models import Metric
from .models import Student, AttendanceRecord,Task,Schedule,Batch,Module


admin.site.register(Metric)


admin.site.register(Batch)
admin.site.register(Module)
admin.site.register(Task)
admin.site.register(Schedule)
admin.site.register(Student)
admin.site.register(AttendanceRecord)

