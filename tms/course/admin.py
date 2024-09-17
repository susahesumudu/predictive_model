from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import Course, Batch, Attendance, CoursePayment, CompletedTask, CompletedModule, Schedule, Module, Task, Session
from .utils import auto_generate_training_plan
# Custom form for AttendanceAdmin to filter only 'Student' group users

# Define a custom action to duplicate tasks
# Define a custom action to duplicate tasks
def duplicate_tasks(modeladmin, request, queryset):
    for task in queryset:
        task.pk = None  # This resets the primary key, so a new record will be created
        task.task_name = task.task_name + " (Copy)"  # Add "Copy" to the task name
        task.save()

duplicate_tasks.short_description = "Duplicate selected tasks"

# Register your Task model in the admin interface
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'total_hours', 'is_theory', 'module']  # Adjust these fields according to your model
    actions = [duplicate_tasks]


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        # Filter student field to only show users in the 'Student' group
        self.fields['student'].queryset = User.objects.filter(groups__name='Student')

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        # Filter student field to only show users in the 'Student' group
        #self.fields['course'].queryset = User.objects.filter(course='course')


class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceForm
    list_display = ('student', 'batch', 'date', 'is_present')
    search_fields = ('student__username', 'batch__batch_name')
    list_filter = ('date', 'is_present')

class ModuleAdmin(admin.ModelAdmin):
    form = ModuleForm
    list_display = ( 'module_name', 'total_theory_hours', 'total_practical_hours')  # Removed the extra space
    search_fields = ('module_name',)  # Wrapped in a tuple
    list_filter = ('module_name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    actions = ['generate_training_plan']

    fieldsets = (
        ('Basic Information', {
            'fields': ( 'course_title', 'course_code', 'is_active')
        }),
        ('Curriculum Details', {
            'fields': ('curriculum_category', 'curriculum_availability', 'batches_per_year', 'duration_months', 'capacity_per_batch')
        }),
        ('Time & Hours', {
            'fields': ('theory_hours', 'practical_hours', 'assignment_hours' )
        }),
        ('Modules & Tasks', {
            'fields': ('total_num_modules', 'total_num_assessments', 'total_num_tasks')  # Correct spelling here
        }),
        ('Entry Requirements', {
            'fields': ('entry_qualification', 'medium', 'delivery_mode', 'course_mode')
        }),
        ('Fees & Equipment', {
            'fields': ('course_fee', 'tools_available', 'equipment_available', 'machinery_available')  # Removed 'is_free'
        }),
        ('Industry & Equivalent Course', {
            'fields': ('industry_sector', 'equivalent_course')
        }),
    )

    readonly_fields = ('course_code',)  # Auto-generated course code
    search_fields = ('course_title',)

  
    list_display = ('course_title', 'course_code', 'course_fee', 'is_active')


    def generate_training_plan(self, request, queryset):
        for course in queryset:
            auto_generate_training_plan(course.id, date.today())
        self.message_user(request, "Training plans generated successfully.")



# Register other models as needed
#admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(CoursePayment)
admin.site.register(CompletedTask)
admin.site.register(CompletedModule)
admin.site.register(Schedule)
admin.site.register(Module,ModuleAdmin)
#admin.site.register(Task)
admin.site.register(Session)

# Register the Attendance model with the admin
admin.site.register(Attendance, AttendanceAdmin)



