from django.contrib import admin
from .models import Booking


@admin.register(Booking)

class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'room',
        'check_in',
        'check_out',
        'booking_status',
        'payment_status'

    )

    list_filter = (
        'booking_status',

        'payment_status'

    )

    search_fields = (

        'customer__full_name',

        'room__room_number'

    )

    ordering = (

        '-created_at',

    )