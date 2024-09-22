from django.contrib import admin

from .models import Student, Teacher, Activity, Attendance, Prediction, Task, Submission

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'attendance_percentage', 'total_marks')
    search_fields = ('name', 'email')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'due_date')
    search_fields = ('name', 'teacher__user__username')
    list_filter = ('due_date',)



admin.site.register(Attendance)
admin.site.register(Prediction)
admin.site.register(Task)
admin.site.register(Submission)

