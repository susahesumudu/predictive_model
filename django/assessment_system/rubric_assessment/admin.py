from django.contrib import admin
from .models import Rubric, Criteria, Student, Assessment,Activity
admin.site.register(Activity)


admin.site.register(Rubric)
admin.site.register(Criteria)
admin.site.register(Student)
admin.site.register(Assessment)

