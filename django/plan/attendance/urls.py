from .views import attendance_list, attendance_dashboard, record_attendance

urlpatterns = [
    path('list/', attendance_list, name='attendance_list'),
    path('dashboard/', attendance_dashboard, name='attendance_dashboard'),
    path('record/', record_attendance, name='record_attendance'),  # For RFID attendance recording
]
