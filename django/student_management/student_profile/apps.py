from django.apps import AppConfig

class StudentProfileConfig(AppConfig):
    name = 'student_profile'

    def ready(self):
        import student_profile.signals

