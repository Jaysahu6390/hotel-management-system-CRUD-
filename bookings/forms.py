from django import forms
from .models import Booking
from rooms.models import Room
from customers.models import Customer
from django.db.models import Q
from django.utils import timezone


class BookingForm(forms.ModelForm):

    class Meta:

        model = Booking

        fields = [

            'customer',
            'room',
            'check_in',
            'check_out',
            'adults',
            'children',
            'booking_status',
            'payment_status'

        ]

        widgets = {

            'customer': forms.Select(attrs={
                'class': 'form-select'
            }),

            'room': forms.Select(attrs={
                'class': 'form-select'
            }),

            'check_in': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'check_out': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'adults': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'children': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'booking_status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'payment_status': forms.Select(attrs={
                'class': 'form-select'
            }),

        }

    def clean(self):

        cleaned_data = super().clean()

        room = cleaned_data.get("room")
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if not room or not check_in or not check_out:
            return cleaned_data

        if check_out <= check_in:
            raise forms.ValidationError(
                "Check-out date must be after check-in."
            )

        overlapping_bookings = Booking.objects.filter(
            room=room,
            booking_status__in=["Booked", "Checked In"]
        ).exclude(
            pk=self.instance.pk
        ).filter(
            Q(check_in__lt=check_out) &
            Q(check_out__gt=check_in)
        )

        if overlapping_bookings.exists():

            raise forms.ValidationError(

                f"Room {room.room_number} is already booked for the selected dates."

            )

        return cleaned_data
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["room"].queryset = Room.objects.filter(
                Q(status="Available") |
                Q(pk=self.instance.room.pk)
            )
        else:
            self.fields["room"].queryset = Room.objects.filter(
                status="Available"
            )