from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "booking",
        "amount",
        "payment_method",
        "payment_date",
    )

    search_fields = (
        "invoice_number",
        "booking__customer__full_name",
    )

    list_filter = (
        "payment_method",
        "payment_date",
    )