from datetime import timedelta, date
from .models import Course, Module, Task, Session

def auto_generate_training_plan(course_id, start_date):
    course = Course.objects.get(id=course_id)
    current_date = start_date

    for module in Module.objects.filter(course=course):
        # Theory sessions
        theory_task = Task.objects.filter(module=module, is_theory=True).first()
        if theory_task:
            theory_hours_left = module.total_theory_hours
            while theory_hours_left > 0:
                session_duration = min(theory_hours_left * 60, 120)  # Max 120 minutes per session
                Session.objects.create(
                    task=theory_task,
                    session_date=current_date,
                    duration_minutes=session_duration
                )
                theory_hours_left -= session_duration / 60
                current_date += timedelta(days=1)
        else:
            print(f"No theory task found for module {module.module_name}")

        # Practical sessions
        practical_task = Task.objects.filter(module=module, is_theory=False).first()
        if practical_task:
            practical_hours_left = module.total_practical_hours
            while practical_hours_left > 0:
                session_duration = min(practical_hours_left * 60, 120)  # Max 120 minutes per session
                Session.objects.create(
                    task=practical_task,
                    session_date=current_date,
                    duration_minutes=session_duration
                )
                practical_hours_left -= session_duration / 60
                current_date += timedelta(days=1)
        else:
            print(f"No practical task found for module {module.module_name}")

    return f"Training plan for course '{course.course_name}' generated successfully."

def auto_generate_lesson_plan(task_id):
    task = Task.objects.get(id=task_id)
    
    # Example data for lesson plan generation (this can be dynamic based on specific task details)
    task.learning_objectives = "At the end of this session, students will be able to..."
    task.teaching_activities = """
    1. Introduction (10 mins): Present key concepts using slides and whiteboard.
    2. Hands-on demonstration (20 mins): Trainer demonstrates using practical tools.
    3. Student practice (30 mins): Students perform the task in pairs.
    4. Group discussion (10 mins): Discuss common issues faced during the task.
    """
    task.resources = "Computers, Projector, Whiteboard, Network Components, etc."
    task.assessment_activities = """
    1. Formative assessment: Monitor student activities and provide feedback.
    2. Summative assessment: Evaluate student's performance using a checklist.
    """
    
    # Save the lesson plan details
    task.save()
