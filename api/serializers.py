from rest_framework import serializers
from customers.models import Customer
from rooms.models import Room
from bookings.models import Booking
from payments.models import Payment


class RoomSerializer(serializers.ModelSerializer):

    class Meta:

        model = Room

        fields = "__all__"

    def validate_room_number(self, value):

        qs = Room.objects.filter(room_number=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():

            raise serializers.ValidationError(
                "Room number already exists."
            )

        return value

    def validate_price(self, value):

        if value <= 0:

            raise serializers.ValidationError(
                "Price must be greater than zero."
            )

        return value



class CustomerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customer

        fields = "__all__"

    def validate_phone(self, value):

        if len(value) != 10:

            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        if not value.isdigit():

            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        return value

from bookings.models import Booking
from datetime import date


class BookingSerializer(serializers.ModelSerializer):

    class Meta:

        model = Booking

        fields = "__all__"

    def validate(self, attrs):

        check_in = attrs["check_in"]

        check_out = attrs["check_out"]

        room = attrs["room"]

        if check_out <= check_in:

            raise serializers.ValidationError(

                "Check-out date must be after check-in."

            )

        overlapping = Booking.objects.filter(

            room=room,

            booking_status="Confirmed",

            check_in__lt=check_out,

            check_out__gt=check_in,

        )

        if self.instance:

            overlapping = overlapping.exclude(
                pk=self.instance.pk
            )

        if overlapping.exists():

            raise serializers.ValidationError(

                "Room is already booked for these dates."

            )

        return attrs
    

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Payment

        fields = "__all__"

    def validate_amount(self, value):

        if value <= 0:

            raise serializers.ValidationError(

                "Payment amount must be greater than zero."

            )

        return value