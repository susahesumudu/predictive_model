from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

def validate_min_students(value):
    """ Custom validator to ensure minimum students per batch """
    if value < 5:  # Example minimum students
        raise ValidationError(f'Minimum number of students is 5.')

def validate_max_students(value):
    """ Custom validator to ensure maximum students per batch """
    if value > 30:  # Example maximum students
        raise ValidationError(f'Maximum number of students is 30.')


class Course(models.Model):
    # Curriculum Category Choices

    CURRICULUM_CATEGORY_CHOICES = [
        ('nvq', 'NVQ'),
        ('nonnvq', 'Non-NVQ'),
        ('nie', 'NIE'),
        ('other', 'Other'),
    ]

    # Unique identifier and descriptive fields for the course
    course_id = models.CharField(max_length=20, unique=True)
    course_title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20, unique=True, blank=True)  # Auto-generated
    is_active = models.BooleanField(default=True, help_text="Uncheck if the course is inactive")

    # Duration and hour tracking fields
    theory_hours = models.PositiveIntegerField(help_text="Total theory hours for the course")
    practical_hours = models.PositiveIntegerField(help_text="Total practical hours for the course")
    assignment_hours = models.PositiveIntegerField(help_text="Total hours for assignments/projects", default=0)
    total_num_modules = models.PositiveIntegerField(help_text="Total number of modules")
    total_num_assessments = models.PositiveIntegerField(help_text="Total number of assessments across modules")
    total_num_tasks = models.PositiveIntegerField(help_text="Total number of tasks across modules")
    duration_months = models.PositiveIntegerField(help_text="Course duration in months (without OJT)")
    
    # Other course information
    entry_qualification = models.CharField(max_length=100, help_text="Entry qualification required")
    medium = models.CharField(max_length=50, choices=[('English', 'English'), ('Sinhala', 'Sinhala'), ('Tamil', 'Tamil')])
    delivery_mode = models.CharField(max_length=50, choices=[('Classroom', 'Classroom'), ('Online', 'Online'), ('Blended', 'Blended')])
    course_mode = models.CharField(max_length=50, choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time')])

    # Curriculum and batch details
     # Curriculum Category (with predefined choices)
    curriculum_category = models.CharField(
        max_length=50, 
        choices=CURRICULUM_CATEGORY_CHOICES, 
        help_text="Select curriculum category"
    )
    curriculum_availability = models.BooleanField(default=True, help_text="Is the curriculum available? (Yes/No)")

    batches_per_year = models.PositiveIntegerField(help_text="Number of batches per annum")
    capacity_per_batch = models.PositiveIntegerField(help_text="Number of students per batch")
    
    # Financial information
    course_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Resources required for the course
    tools_available = models.TextField(help_text="List of tools available", blank=True)
    equipment_available = models.TextField(help_text="List of equipment available", blank=True)
    machinery_available = models.TextField(help_text="List of machinery available", blank=True)
    
    # Industry-related information
    industry_sector = models.CharField(max_length=100, help_text="Select industry/sector")
    equivalent_course = models.CharField(max_length=100, blank=True, help_text="Equivalent course (if any)")
    
    # Auto-generate course code from title if not provided
    def save(self, *args, **kwargs):
        if not self.course_code:
            words = self.course_title.split()
            self.course_code = ''.join([word[0].upper() for word in words])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_title} ({self.course_code})"

    # Calculate total hours for the course
    def calculate_total_hours(self):
        return self.theory_hours + self.practical_hours + self.assignment_hours

    # Generate course plan based on input parameters (e.g., days per week, hours per day)
    def generate_course_plan(self, days_per_week, hours_per_day):
        total_hours = self.calculate_total_hours()
        total_weeks = self.duration_months * 4  # Assuming ~4 weeks per month
        total_days = total_weeks * days_per_week
        total_available_hours = total_days * hours_per_day

        if total_hours > total_available_hours:
            raise ValidationError(f"Total hours ({total_hours}) exceed available hours ({total_available_hours})!")

        # Distribute hours among modules
        hours_per_module = total_hours / self.total_num_modules

        modules = Module.objects.filter(course=self)
        for module in modules:
            module.total_theory_hours = self.theory_hours // self.total_num_modules
            module.total_practical_hours = self.practical_hours // self.total_num_modules
            module.save()


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=255)
    total_theory_hours = models.PositiveIntegerField(help_text="Total theory hours for this module")
    total_practical_hours = models.PositiveIntegerField(help_text="Total practical hours for this module")
    total_num_assessments = models.PositiveIntegerField(help_text="Total number of assessments for this module")
    total_num_tasks = models.PositiveIntegerField(help_text="Total number of tasks for this module")

    def __str__(self):
        return f"{self.module_name} (Course: {self.course.course_title})"

    def clean(self):
        """
        Custom validation to ensure the module's hours, assessments, and tasks
        don't exceed the total limits defined in the related course.
        """
        # Get the current sums of hours, assessments, and tasks for the course, excluding the current module when editing
        current_theory_hours = Module.objects.filter(course=self.course).exclude(id=self.id).aggregate(models.Sum('total_theory_hours'))['total_theory_hours__sum'] or 0
        current_practical_hours = Module.objects.filter(course=self.course).exclude(id=self.id).aggregate(models.Sum('total_practical_hours'))['total_practical_hours__sum'] or 0
        current_assessments = Module.objects.filter(course=self.course).exclude(id=self.id).aggregate(models.Sum('total_num_assessments'))['total_num_assessments__sum'] or 0
        current_tasks = Module.objects.filter(course=self.course).exclude(id=self.id).aggregate(models.Sum('total_num_tasks'))['total_num_tasks__sum'] or 0

        # Check if adding this module would exceed the course's total limits
        if current_theory_hours + self.total_theory_hours > self.course.theory_hours:
            raise ValidationError(f"Adding {self.total_theory_hours} hours exceeds the course's total theory hours limit of {self.course.theory_hours} hours.")
        
        if current_practical_hours + self.total_practical_hours > self.course.practical_hours:
            raise ValidationError(f"Adding {self.total_practical_hours} hours exceeds the course's total practical hours limit of {self.course.practical_hours} hours.")
        
        if current_assessments + self.total_num_assessments > self.course.total_num_assessments:
            raise ValidationError(f"Adding {self.total_num_assessments} assessments exceeds the course's total assessment limit of {self.course.total_num_assessments} assessments.")
        
        if current_tasks + self.total_num_tasks > self.course.total_num_tasks:
            raise ValidationError(f"Adding {self.total_num_tasks} tasks exceeds the course's total task limit of {self.course.total_num_tasks} tasks.")

    def save(self, *args, **kwargs):
        """
        Custom save method to ensure that the module count is checked only when adding new modules,
        but allows editing existing ones without triggering the module count limit.
        """
        # Check if the module is new (i.e., it's being created)
        if not self.pk:  # New module creation
            current_module_count = Module.objects.filter(course=self.course).count()

            # Check if adding this module would exceed the number of modules allowed
            if current_module_count >= self.course.total_num_modules:
                raise ValidationError(f"Cannot add more modules than the specified limit ({self.course.total_num_modules}) for the course: {self.course.course_title}.")
        
        # Run custom validation for hours, assessments, and tasks (applies for both add and edit)
        self.clean()
        
        # Save the module
        super().save(*args, **kwargs)


class Task(models.Model):
    # Tasks are associated with a module
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    # Basic task information
    task_name = models.CharField(max_length=255)
    total_hours = models.PositiveIntegerField(help_text="Total hours for this task")
    is_theory = models.BooleanField(default=True, help_text="Is this a theory task?")

    # Additional fields for lesson plans (these can be optional)
    learning_objectives = models.TextField(help_text="What students will learn", blank=True, null=True)
    teaching_activities = models.TextField(help_text="Teaching activities for the task", blank=True, null=True)
    resources = models.TextField(help_text="Required resources and materials", blank=True, null=True)
    assessment_activities = models.TextField(help_text="Assessment activities to evaluate student learning", blank=True, null=True)

    def __str__(self):
        return f"{self.task_name} ({'Theory' if self.is_theory else 'Practical'})"

    def clean(self):
        """
        Validation to ensure that the total number of tasks within a module does not exceed
        the number of tasks allocated for the module.
        """
        # Check how many tasks are already associated with this module
        current_task_count = Task.objects.filter(module=self.module).exclude(id=self.id).count()

        # Check if adding this task would exceed the number of tasks allowed for the module
        if current_task_count >= self.module.total_num_tasks:
            raise ValidationError(
                f"Cannot add more tasks. The module '{self.module.module_name}' already has "
                f"{current_task_count} tasks, and the limit is {self.module.total_num_tasks}."
            )

    def save(self, *args, **kwargs):
        # Run validation before saving
        self.clean()

        # Proceed to save the task
        super().save(*args, **kwargs)


class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_batches', limit_choices_to={'groups__name': 'Teacher'})
    students = models.ManyToManyField(User, related_name='enrolled_batches', limit_choices_to={'groups__name': 'Student'}, blank=True)
    demos = models.ManyToManyField(User, related_name='demo_batches', limit_choices_to={'groups__name': 'Lab Assistant'}, blank=True)
    min_students = models.PositiveIntegerField(validators=[validate_min_students])
    max_students = models.PositiveIntegerField(validators=[validate_max_students])

    def __str__(self):
        return f"{self.batch_name} - {self.course.course_title}"


class CoursePayment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment by {self.student.username} for {self.batch}"


class CompletedTask(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date_completed = models.DateField()

    def __str__(self):
        return f"{self.task_name} completed by {self.student.username} for {self.batch}"


class CompletedModule(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=100)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date_completed = models.DateField()

    def __str__(self):
        return f"{self.module_name} completed by {self.student.username} for {self.batch}"


class Attendance(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"Attendance for {self.student.username} on {self.date}"



class Schedule(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    module_name = models.ForeignKey(Module, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.module_name} ({self.start_date} to {self.end_date})"




class Session(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    session_date = models.DateField()
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"Session on {self.session_date} for task {self.task.task_name} ({self.duration_minutes} minutes)"


