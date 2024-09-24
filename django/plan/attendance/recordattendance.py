from django.http import JsonResponse
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from .models import AttendanceRecord, StudentProfile

def record_attendance(request):
    # Get RFID tag from request
    rfid_tag = request.GET.get('rfid_tag', None)

    if not rfid_tag:
        return JsonResponse({'error': 'RFID tag is required'}, status=400)

    # Find the student by RFID tag
    student_profile = get_object_or_404(StudentProfile, rfid_tag=rfid_tag)

    # Create an attendance record for the student
    AttendanceRecord.objects.create(student=student_profile.user, check_in_time=now(), is_present=True)

    return JsonResponse({'status': 'Attendance recorded successfully'})

