from django.shortcuts import render

from .models import Course, Module, Task, Activity
import random

def create_activities():
    courses = {
        "Web Development": {
            "modules": ["HTML & CSS", "JavaScript", "Backend Development"],
            "tasks": {
                "HTML & CSS": ["Learn HTML", "Learn CSS", "Responsive Design"],
                "JavaScript": ["Basic JS Syntax", "DOM Manipulation", "AJAX"],
                "Backend Development": ["Setting up Flask", "Database Integration", "API Development"],
            }
        },
        "Data Science": {
            "modules": ["Introduction to Python", "Statistics", "Machine Learning"],
            "tasks": {
                "Introduction to Python": ["Python Basics", "Data Structures", "Functions and OOP"],
                "Statistics": ["Descriptive Stats", "Probability", "Hypothesis Testing"],
                "Machine Learning": ["Supervised Learning", "Unsupervised Learning", "Neural Networks"],
            }
        }
    }

    activity_types = ["exercise", "work_project", "assignment", "assessment", "lecture", "discussion"]
    session_types = ["theory", "practical"]

    for course_name, course_data in courses.items():
        course = Course.objects.create(name=course_name, description=f"Course on {course_name}")
        
        for module_name in course_data["modules"]:
            module = Module.objects.create(course=course, title=module_name)

            for task_name in course_data["tasks"][module_name]:
                task = Task.objects.create(module=module, title=task_name, description=f"{task_name} description")
                
                for i in range(10):  # Create 10 activities per task
                    Activity.objects.create(
                        task=task,
                        title=f"{task_name} Activity {i + 1}",
                        activity_type=random.choice(activity_types),
                        session_type=random.choice(session_types),
                        duration_hours=round(random.uniform(1, 4), 1)  # Random duration between 1 to 4 hours
                    )

