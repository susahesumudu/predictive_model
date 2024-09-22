from django.shortcuts import render
from .models import Student
from .simple_model import predict_performance

# View to display a student's information and performance prediction
def student_performance_view(request, student_id):
    student = Student.objects.get(id=student_id)
    prediction = predict_performance(
        student.attendance_rate,
        student.assignment_score,
        student.exercise_completion,
        student.engagement
    )
    return render(request, 'predictions/student_performance.html', {'student': student, 'prediction': prediction})


