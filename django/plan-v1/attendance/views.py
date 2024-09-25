from django.shortcuts import render
from .models import AttendanceRecord

def attendance_list(request):
    # Get attendance records for the current student
    if request.user.is_authenticated:
        attendance_records = AttendanceRecord.objects.filter(student=request.user)
    else:
        attendance_records = []

    return render(request, 'attendance/attendance_list.html', {
        'attendance_records': attendance_records,
    })

def attendance_dashboard(request):
    # Get all attendance records (for teachers/admin)
    attendance_records = AttendanceRecord.objects.all()

    return render(request, 'attendance/dashboard.html', {
        'attendance_records': attendance_records,
    })

