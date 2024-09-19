from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from .models import Course, Batch, Schedule, Session, Course,Module, Task
from django.contrib.auth.models import User
from datetime import timedelta, date
import plotly.express as px
from django.shortcuts import redirect  # Add this import
from .utils import auto_generate_training_plan
from django.views.generic import TemplateView
from django import forms

from django.views.generic import FormView
from django.urls import reverse_lazy
from django import forms


from django.views.generic import View

from .utils import auto_generate_lesson_plan

class CourseListView(ListView):
    model = Course
    template_name = 'course/course_list.html'
    context_object_name = 'courses'


class BatchListView(ListView):
    model = Batch
    template_name = 'course/batch_list.html'
    context_object_name = 'batches'


class BatchDetailView(DetailView):
    model = Batch
    template_name = 'course/batch_detail.html'
    context_object_name = 'batch'


class BatchCreateView(CreateView):
    model = Batch
    fields = ['course', 'batch_name', 'start_date', 'end_date', 'teacher', 'students']
    template_name = 'course/batch_form.html'
    success_url = '/batches/'  # redirect to batch list after creation


class BatchUpdateView(UpdateView):
    model = Batch
    fields = ['course', 'batch_name', 'start_date', 'end_date', 'teacher', 'students']
    template_name = 'course/batch_form.html'
    success_url = '/batches/'  # redirect to batch list after update



# views.py
class GenerateScheduleView(DetailView):
    model = Course
    template_name = 'generate_schedule.html'
    context_object_name = 'course'

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        self.generate_course_schedule(course)
        return redirect('gantt_chart', course_id=course.id)

    def generate_course_schedule(self, course):
        start_date = date.today()
        course_duration_in_weeks = 24
        modules = Module.objects.filter(course=course)  # Get actual modules associated with the course
        weeks_per_module = course_duration_in_weeks / len(modules)

        current_date = start_date

        # Delete existing schedules for this course through module relation
        Schedule.objects.filter(module_name__course=course).delete()  # Corrected field reference

        for module in modules:
            end_date = current_date + timedelta(weeks=weeks_per_module)

            # Create a new schedule entry
            Schedule.objects.create(
                module_name=module,  # Use the actual module object from the database
                start_date=current_date,
                end_date=end_date
            )

            current_date = end_date



class GanttChartView(TemplateView):
    template_name = 'gantt_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        schedules = Schedule.objects.filter(course_id=course_id)

        # Prepare data for the Gantt chart
        df = []
        for schedule in schedules:
            df.append({
                'Task': schedule.module_name,
                'Start': schedule.start_date,
                'Finish': schedule.end_date
            })

        # Generate Gantt chart with Plotly
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", title="Course Schedule")
        fig.update_yaxes(categoryorder="total ascending")

        # Add the Gantt chart HTML to the context
        context['gantt_plot'] = fig.to_html()
        return context



class TrainingPlanForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select Course")

class GenerateTrainingPlanView(FormView):
    template_name = 'generate_training_plan.html'
    form_class = TrainingPlanForm
    success_url = reverse_lazy('training_plan_confirmation')

    def form_valid(self, form):
        course = form.cleaned_data['course']
        start_date = form.cleaned_data['start_date']
        auto_generate_training_plan(course.id, start_date)
        return super().form_valid(form)



class TrainingPlanConfirmationView(TemplateView):
    template_name = 'training_plan_confirmation.html'



class TrainingPlanListView(ListView):
    model = Session
    template_name = 'training_plan_list.html'  # Create this template
    context_object_name = 'sessions'
    
    def get_queryset(self):
        # Filter sessions by course
        course_id = self.kwargs['course_id']
        return Session.objects.filter(task__module__course_id=course_id).order_by('session_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs['course_id'])
        return context


class GenerateLessonPlanView(View):
    def post(self, request, *args, **kwargs):
        module_id = self.kwargs['module_id']
        module = Module.objects.get(id=module_id)
        
        # Generate lesson plan for each task in the module
        for task in module.task_set.all():
            auto_generate_lesson_plan(task.id)
        
        return redirect('module_detail', module_id=module_id)

from django.views.generic import DetailView


class ModuleDetailView(DetailView):
    model = Module
    template_name = 'module_lesson_plans.html'
    context_object_name = 'module'

from django.http import JsonResponse
from .models import User

def get_students(request):
    batch_id = request.GET.get('batch_id')
    students = User.objects.filter(enrolled_batches__id=batch_id, groups__name='Student')
    student_list = [{'id': student.id, 'name': student.username} for student in students]
    return JsonResponse({'students': student_list})

