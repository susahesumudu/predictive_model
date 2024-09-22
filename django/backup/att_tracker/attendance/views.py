from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Session, Attendance
from attendance.utils import create_recurring_sessions

# Call the function wherever needed
create_recurring_sessions()


def mark_attendance(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    students = Student.objects.all()
    
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            Attendance.objects.create(student=student, session=session, status=status)
        return redirect('attendance_report', session_id=session.id)
    
    return render(request, 'attendance/mark_attendance.html', {'session': session, 'students': students})

def attendance_report(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    attendance_records = Attendance.objects.filter(session=session)
    
    return render(request, 'attendance/attendance_report.html', {'session': session, 'attendance_records': attendance_records})

