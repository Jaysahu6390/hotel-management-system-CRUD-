from django.db import models
from customers.models import Customer
from rooms.models import Room


class Booking(models.Model):

    STATUS_BOOKED = "Booked"
    STATUS_CHECKED_IN = "Checked In"
    STATUS_CHECKED_OUT = "Checked Out"
    STATUS_CANCELLED = "Cancelled"


    BOOKING_STATUS = [
        ("Booked", "Booked"),
        ("Checked In", "Checked In"),
        ("Checked Out", "Checked Out"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )

    room = models.ForeignKey(
        Room,       
        on_delete=models.PROTECT
    )

    check_in = models.DateField()

    check_out = models.DateField()

    adults = models.PositiveIntegerField(default=1)

    children = models.PositiveIntegerField(default=0)

    booking_status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default="Booked"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - Room {self.room.room_number}"