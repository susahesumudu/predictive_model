# views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course, Module, Task, Activity, Submission,GradingRubric, Activity

from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404

from django.shortcuts import redirect

from django.utils import timezone

from .forms import SubmissionForm, MarksForm,GradingRubricForm


#Home Page
class HomePageView(TemplateView):
    template_name = 'home.html'



#---------------------------Courses---------------------------------------------------------

# 1. ListView: To list all courses
class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'  # to use 'courses' in the template
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is in the Teacher group
        context['is_teacher'] = self.request.user.groups.filter(name='Teacher').exists()
        return context

# 2. DetailView: To view details of a single course
class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is in the Teacher group
        context['is_teacher'] = self.request.user.groups.filter(name='Teacher').exists()
        return context

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    fields = ['title', 'description']
    template_name = 'course/course_form.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        # Only staff can create courses
        return self.request.user.groups.filter(name='Staff').exists()

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    fields = ['title', 'description']
    template_name = 'course/course_form.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        # Only staff can update courses
        return self.request.user.groups.filter(name='Staff').exists()

class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'course/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        # Only staff can delete courses
        return self.request.user.groups.filter(name='Staff').exists()




#---------------------------Module---------------------------------------------------------

class ModuleCreateView(CreateView):
    model = Module
    template_name = 'module/module_form.html'
    fields = ['title', 'description', 'course']
    success_url = reverse_lazy('module_list')

class ModuleUpdateView(UpdateView):
    model = Module
    template_name = 'module/module_form.html'
    fields = ['title', 'description', 'course']
    success_url = reverse_lazy('module_list')

class ModuleDeleteView(DeleteView):
    model = Module
    template_name = 'module/module_confirm_delete.html'
    success_url = reverse_lazy('module_list')

class ModuleDetailView(DetailView):
    model = Module
    template_name = 'module/module_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is in the Teacher group
        context['is_teacher'] = self.request.user.groups.filter(name='Teacher').exists()
        return context

class ModuleListView(ListView):
    model = Module
    template_name = 'module/module_list.html'
    context_object_name = 'modules'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is in the Teacher group
        context['is_teacher'] = self.request.user.groups.filter(name='Teacher').exists()
        return context


#---------------------------Tasks---------------------------------------------------------

class TaskCreateView(CreateView):
    model = Task
    template_name = 'task/task_form.html'
    fields = ['title', 'description', 'module']
    success_url = reverse_lazy('task_list')

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'task/task_form.html'
    fields = ['title', 'description', 'module']
    success_url = reverse_lazy('task_list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is in the Teacher group
        context['is_teacher'] = self.request.user.groups.filter(name='Teacher').exists()
        return context


class TaskListView(ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is in the Teacher group
        context['is_teacher'] = self.request.user.groups.filter(name='Teacher').exists()
        return context



#---------------------------Activity---------------------------------------------------------



class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activity/activity_list.html'
    context_object_name = 'activities'
    

# Create a new activity
class ActivityCreateView(CreateView):
    model = Activity
    fields = ['task', 'title', 'description', 'activity_type', 'grading_rubric', 'publish_grading_rubric',
              'submission_deadline', 'session_type']
    template_name = 'activity/activity_form.html'
    success_url = reverse_lazy('activity_list')

    def test_func(self):
        # Only teachers can add activities
        return self.request.user.groups.filter(name='Teacher').exists()

# Update an existing activity
class ActivityUpdateView(UpdateView):
    model = Activity
    fields = ['task', 'title', 'description', 'activity_type', 'grading_rubric', 'publish_grading_rubric',
              'submission_deadline', 'session_type']
    template_name = 'activity/activity_form.html'
    success_url = reverse_lazy('activity_list')

    def test_func(self):
        # Only teachers can update activities
        return self.request.user.groups.filter(name='Teacher').exists()

class ActivityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Activity
    template_name = 'activity/activity_confirm_delete.html'
    success_url = reverse_lazy('activity_list')

    def test_func(self):
        # Only teachers can delete activities
        return self.request.user.groups.filter(name='Teacher').exists()

class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = 'activity/activity_detail.html'
    context_object_name = 'activity'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = self.object  # Ensures the activity object is passed
        activity = self.get_object()
        # Fetch all submissions for this activity
        submissions = activity.submissions.all()  # Assuming `submissions` is a related name in the `Activity` model
        context['submissions'] = activity.submissions.all() 
        context['is_teacher'] = self.request.user.groups.filter(name='Teacher').exists()
        context['is_student'] = self.request.user.groups.filter(name='Student').exists()
        user = self.request.user
        context['has_submitted'] = self.object.submissions.filter(student=user).exists()
        return context   
       

# Handle student submission
class SubmissionCreateView(CreateView):  # Change FormView to CreateView
    model = Submission
    form_class = SubmissionForm
    template_name = 'activity/submit_activity.html'
    
    def form_valid(self, form):
        if not self.request.user.groups.filter(name='Student').exists():
            return self.handle_no_permission()  # Restrict access if the user is not a student

        activity = get_object_or_404(Activity, pk=self.kwargs['pk'])
        submission = form.save(commit=False)  # Save form without committing yet
        submission.activity = activity
        submission.student = self.request.user  # Assuming the student is logged in
        submission.submitted_at = timezone.now()
        submission.end_time = timezone.now()  # Set end_time if it's required
        submission.save()  # Save the submission to the database
        return redirect('activity_detail', pk=activity.pk)  # Redirect to activity detail page

    def get_success_url(self):
        return reverse_lazy('activity_list')  # URL to redirect after success

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = get_object_or_404(Activity, pk=self.kwargs['pk'])  # Add activity to context
        return context



# Grade a submission (teacher's task)
class SubmissionGradeView(UpdateView):
    model = Submission
    form_class = MarksForm
    template_name = 'activity/grade_submission.html'
    
    def get_success_url(self):
        return reverse_lazy('activity_list')


# Create Rubric for an Activity
class RubricCreateView(CreateView):
    model = GradingRubric
    form_class = GradingRubricForm
    template_name = 'activity/rubric_form.html'

    def form_valid(self, form):
        # Attach the rubric to the specific activity
        activity = get_object_or_404(Activity, pk=self.kwargs['pk'])
        form.instance.activity = activity
        return super().form_valid(form)

    # Correctly return the success URL
    def get_success_url(self):
        return reverse_lazy('activity_detail', kwargs={'pk': self.kwargs['pk']})


# Update Rubric for an Activity
class RubricUpdateView(UpdateView):
    model = GradingRubric
    form_class = GradingRubricForm
    template_name = 'activity/rubric_form.html'

    def get_success_url(self):
        return reverse_lazy('activity_detail', kwargs={'pk': self.object.activity.pk})


