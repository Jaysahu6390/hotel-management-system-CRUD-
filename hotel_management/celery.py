import os
from celery.schedules import crontab
from celery import Celery

# Set Django settings module
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "hotel_management.settings"
)

# Create Celery app
app = Celery("hotel_management")

# Load settings from Django
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

# Auto-discover tasks.py in installed apps
app.autodiscover_tasks()

app.conf.beat_schedule = {

    "send-booking-reminders-every-day": {

        "task": "bookings.tasks.send_booking_reminders",

        "schedule": crontab(hour=9, minute=0),

    },
}