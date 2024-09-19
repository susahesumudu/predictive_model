from django.utils import timezone
from .models import ScheduledSession
from datetime import timedelta

def create_recurring_sessions():
    sessions = ScheduledSession.objects.filter(repeat_until__gte=timezone.now().date())

    for session in sessions:
        next_session_date = session.start_time
        while next_session_date.date() <= session.repeat_until:
            if session.frequency == 'D':
                next_session_date += timedelta(days=1)
            elif session.frequency == 'W':
                next_session_date += timedelta(weeks=1)
            elif session.frequency == 'M':
                next_session_date += timedelta(weeks=4)

            # Check if session already exists
            if not ScheduledSession.objects.filter(start_time=next_session_date).exists():
                ScheduledSession.objects.create(
                    session_name=session.session_name,
                    start_time=next_session_date,
                    end_time=next_session_date + (session.end_time - session.start_time),
                    frequency=session.frequency,
                    repeat_until=session.repeat_until
                )

