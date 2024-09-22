from django.core.management.base import BaseCommand
from attendance.models import create_recurring_sessions  # if in models
# or
from attendance.utils import create_recurring_sessions  # if in utils.py

class Command(BaseCommand):
    help = 'Automatically create recurring sessions based on frequency'

    def handle(self, *args, **kwargs):
        create_recurring_sessions()
        self.stdout.write(self.style.SUCCESS('Successfully created recurring sessions'))

