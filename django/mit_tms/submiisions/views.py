from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView,UpdateView
from .models import Exercise, Task,Submission
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import Batch
from .forms import BatchForm,TaskForm
from django.views.generic import View



from django.core.files.storage import FileSystemStorage



class BatchCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'submiisions/batch_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name='Teacher').exists()  # Only teachers can create/edit batches

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.groups.filter(name='Teacher').exists():
            kwargs['initial']['teacher'] = self.request.user
        return kwargs


class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'submiisions/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Check if the user is in the 'Teacher' group
        is_teacher = user.groups.filter(name='Teacher').exists()
        context['is_teacher'] = is_teacher

        # Fetch all tasks if the user is a teacher
        if is_teacher:
            context['exercises'] = Task.objects.filter(task_type='Exercise')
            context['assignments'] = Task.objects.filter(task_type='Assignment')
            context['projects'] = Task.objects.filter(task_type='Project')

        return context


class ScheduleTaskView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'submiisions/schedule_task.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.created_by = self.request.user  # Automatically set the teacher as the creator
        task.save()
        return super().form_valid(form)


class ReviewExerciseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Exercise
    template_name = 'submiisions/review_exercises.html'
    context_object_name = 'exercises'

    def test_func(self):
        return self.request.user.groups.filter(name='Teachers').exists()

    def get_queryset(self):
        return Exercise.objects.filter(status="Pending")


class ReviewExerciseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Exercise
    template_name = 'submissions/review_exercise.html'
    context_object_name = 'exercise'

    def test_func(self):
        return self.request.user.groups.filter(name='Teachers').exists()

    def post(self, request, *args, **kwargs):
        exercise = self.get_object()
        exercise.teacher_feedback = request.POST.get('teacher_feedback')
        exercise.grade = request.POST.get('grade', None)
        exercise.status = 'Reviewed'
        exercise.save()
        return redirect('review_exercises')

class SubmitExerciseView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Exercise
    template_name = 'submissions/submit_exercise.html'
    fields = ['level_of_completion', 'quality_of_work', 'learning_outcome', 'challenges']
    success_url = reverse_lazy('submit_exercise')

    def test_func(self):
        return self.request.user.groups.filter(name='Students').exists()

    def form_valid(self, form):
        task_id = self.request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id)

        submission_time = timezone.now()
        completed_on_time = "Late" if submission_time > task.submission_deadline else "On Time"
        
        form.instance.student = self.request.user  # Use the current logged-in student
        form.instance.exercise_title = task.title
        form.instance.submission_time = submission_time
        form.instance.completed_on_time = completed_on_time
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()  # Pass all tasks to the template
        return context



class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'submiisions/student_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user

        # Get all batches the student is part of
        student_batches = student.student_batches.all()  # ManyToMany relationship for batches

        # Get all tasks related to the student's batch
        tasks = Task.objects.filter(batch__in=student_batches)

        # Get all submissions made by the student
        submissions = Submission.objects.filter(student=student)

        context['tasks'] = tasks
        context['submissions'] = submissions
        return context



class UploadSubmissionView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        student = request.user

        # Handle file upload
        if 'file' in request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)

            # Create or update the submission record
            Submission.objects.create(student=student, task=task, file=filename)

        return redirect('student_dashboard')


