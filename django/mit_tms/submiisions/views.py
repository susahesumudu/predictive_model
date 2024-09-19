# schedule/views.py

from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from .models import Exercise, Task
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class SubmitExerciseView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Exercise
    template_name = 'submissions/submit_exercise.html'
    fields = ['level_of_completion', 'quality_of_work', 'learning_outcome', 'challenges']
    success_url = reverse_lazy('submit_exercise')

    def test_func(self):
        return self.request.user.groups.filter(name='Students').exists()

    def form_valid(self, form):
        form.instance.student_name = self.request.POST.get('student_name')  # Get student name from POST data
        task_id = self.request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        submission_time = timezone.now()
        completed_on_time = "Late" if submission_time > task.submission_deadline else "On Time"

        form.instance.exercise_title = task.title
        form.instance.submission_time = submission_time
        form.instance.completed_on_time = completed_on_time
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()  # Pass all tasks to the template
        return context


# schedule/views.py

class ReviewExerciseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Exercise
    template_name = 'submissions/review_exercises.html'
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
        exercise.grade = request.POST.get('grade')
        exercise.status = 'Reviewed'
        exercise.save()
        return redirect('review_exercises')




