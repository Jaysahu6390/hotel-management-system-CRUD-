from django.db import models
from bookings.models import Booking
from django.utils import timezone

class Payment(models.Model):

    PAYMENT_METHODS = [
        ("Cash", "Cash"),
        ("Card", "Card"),
        ("UPI", "UPI"),
        ("Net Banking", "Net Banking"),
    ]
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    invoice_number = models.CharField(
        max_length=20,
        unique=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )
    payment_date = models.DateField(auto_now_add=True)
    remarks = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.invoice_number:

            last_id = Payment.objects.count() + 1

            self.invoice_number = (
                f"INV{timezone.now().year}{last_id:05d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number