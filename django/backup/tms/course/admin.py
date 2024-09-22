from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import Course, Batch, Attendance, CoursePayment, CompletedTask, CompletedModule, Schedule, Module, Task, Session,SessionSetting,Lesson
from .utils import auto_generate_training_plan


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




class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        # Filter student field to only show users in the 'Student' group
        #self.fields['course'].queryset = User.objects.filter(course='course')


class ModuleAdmin(admin.ModelAdmin):
    form = ModuleForm
    list_display = ( 'module_name', 'total_theory_hours', 'total_practical_hours')  # Removed the extra space
    search_fields = ('module_name',)  # Wrapped in a tuple
    list_filter = ('module_name',)

def duplicate_tasks(modeladmin, request, queryset):
    for task in queryset:
        task.pk = None  # This resets the primary key, so a new record will be created
        task.task_name = task.task_name + " (Copy)"  # Add "Copy" to the task name
        task.save()



# Register your Task model in the admin interface
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'total_hours', 'module']  # Adjust these fields according to your model
    actions = [duplicate_tasks]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['lesson_title']
    filter_horizontal = ['tasks']  # Allows selection of multiple tasks


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_date', 'session_type', 'start_time', 'duration_minutes', 'end_time', 'trainer_name', 'get_tasks']
    
    def get_tasks(self, obj):
        return ", ".join([task.task_name for task in obj.lesson.tasks.all()])
    get_tasks.short_description = 'Tasks'


@admin.register(SessionSetting)
class SessionSettingAdmin(admin.ModelAdmin):
    list_display = ['max_duration_minutes']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['batch', 'student', 'date', 'is_present']

    def __init__(self, *args, **kwargs):
        batch_id = kwargs.pop('batch_id', None)
        super(AttendanceForm, self).__init__(*args, **kwargs)

        # If a batch is selected, filter the students to show only those in the selected batch
        if batch_id:
            self.fields['student'].queryset = User.objects.filter(
                enrolled_batches__id=batch_id, groups__name='Student'
            )
        else:
            # If no batch is selected, don't show any students initially
            self.fields['student'].queryset = User.objects.none()


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceForm
    list_display = ('batch', 'student', 'date', 'is_present')
    search_fields = ('student__username', 'batch__batch_name')
    list_filter = ('date', 'is_present')

    # Override the get_form method to pass batch_id to the form during record creation/editing
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)

        # If we're editing an existing attendance record, pass the batch to filter students
        if obj:
            form = form(request, batch_id=obj.batch_id)
        elif 'batch' in request.GET:
            # If we're adding a new attendance record and a batch is selected
            batch_id = request.GET.get('batch')
            form = form(request, batch_id=batch_id)

        return form






# Register other models as needed
#admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(CoursePayment)
admin.site.register(CompletedTask)
admin.site.register(CompletedModule)
admin.site.register(Schedule)
admin.site.register(Module,ModuleAdmin)




# Register the Attendance model with the admin
#admin.site.register(Attendance, AttendanceAdmin)


