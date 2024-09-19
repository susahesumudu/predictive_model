from django.contrib import admin
from .models import Student, Assignment

# Inline form for assignments under Student
class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1  # Number of blank forms

# Customizing the Student admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'attendance_rate', 'assignment_score', 'exercise_completion', 'engagement', 'total_score', 'performance_status')
    search_fields = ('name',)
    list_filter = ('attendance_rate', 'assignment_score')
    readonly_fields = ('total_score',)
    list_editable = ('attendance_rate', 'assignment_score')
    fieldsets = (
        (None, {'fields': ('name', 'attendance_rate', 'assignment_score')}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('exercise_completion', 'engagement')}),
    )
    inlines = [AssignmentInline]  # Add the inline for assignments

    def total_score(self, obj):
        return (obj.attendance_rate * 100) + obj.assignment_score

    total_score.short_description = "Total Score"

    def performance_status(self, obj):
        if obj.attendance_rate > 0.7 and obj.assignment_score > 70:
            return "On Track"
        else:
            return "At Risk"
    
    performance_status.short_description = "Performance Status"

# Register the models
admin.site.register(Student, StudentAdmin)
admin.site.register(Assignment)  # Register the Assignment model

