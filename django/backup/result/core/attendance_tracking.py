from .models import Student, Attendance

def track_attendance(rfid_tag):
    student = Student.objects.get(rfid_tag=rfid_tag)
    Attendance.objects.create(student=student, present=True)
    return "Attendance Recorded"

