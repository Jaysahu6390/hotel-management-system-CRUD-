from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from .models import Booking


@shared_task
def send_booking_reminders():

    tomorrow = timezone.localdate() + timedelta(days=1)

    bookings = Booking.objects.select_related("customer").filter(
        check_in=tomorrow,
        booking_status="Confirmed",
    )

    sent_count = 0

    for booking in bookings:

        customer = booking.customer

        send_mail(
            subject="Booking Reminder",
            message=(
                f"Dear {customer.full_name},\n\n"
                f"This is a reminder that your check-in is scheduled for {booking.check_in}.\n"
                f"We look forward to welcoming you!"
            ),
            from_email=None,
            recipient_list=[customer.email],
            fail_silently=False,
        )

        sent_count += 1

    return f"{sent_count} reminder email(s) sent."