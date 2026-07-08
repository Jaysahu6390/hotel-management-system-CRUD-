from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import BookingForm
from .models import Booking
from django.shortcuts import get_object_or_404
from rooms.models import Room
from core.email_service import send_booking_email,send_cancel_email
from audit.utils import create_log

@login_required
def create_booking(request):

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            room = form.cleaned_data["room"]

            room_already_booked = Booking.objects.filter(
                room=room,
                booking_status__in=[
                    Booking.STATUS_BOOKED,
                    Booking.STATUS_CHECKED_IN,
                ]
            ).exists()

            if room_already_booked:

                messages.error(
                    request,
                    "This room is already booked or occupied."
                )

                return render(
                    request,
                    "bookings/booking_form.html",
                    {
                        "form": form,
                        "title": "Create Booking",
                    }
                )

            booking = form.save()
            create_log(
                request,
                "CREATE",
                "Booking",
                f"Booking created for Room {booking.room.room_number}.",
                booking.id
            )
            send_booking_email(booking)

            room.status = "Occupied"
            room.save()

            messages.success(
                request,
                "Booking created successfully."
            )

            return redirect("booking_list")

    else:

        form = BookingForm()

    return render(
        request,
        "bookings/booking_form.html",
        {
            "form": form,
            "title": "Create Booking",
        }
    )

@login_required
def booking_list(request):

    search = request.GET.get("search", "")

    bookings = Booking.objects.select_related(
        "customer",
        "room"
    ).order_by("-created_at")

    if search:
        bookings = bookings.filter(
            Q(customer__full_name__icontains=search) |
            Q(room__room_number__icontains=search) |
            Q(booking_status__icontains=search)
        )

    paginator = Paginator(bookings, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
    }

    return render(
        request,
        "bookings/booking_list.html",
        context
    )

@login_required
def update_booking(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk
    )

    old_room = booking.room

    if request.method == "POST":

        form = BookingForm(
            request.POST,
            instance=booking
        )

        if form.is_valid():

            booking = form.save()
            create_log(
                request,
                "UPDATE",
                "Booking",
                f"Booking {booking.id} updated.",
                booking.id
            )

            # Release old room if room changed
            if old_room != booking.room:
                old_room.status = "Available"
                old_room.save()

            # Update new room status
            if booking.booking_status == "Checked In":
                booking.room.status = "Occupied"
            elif booking.booking_status in [
                "Checked Out",
                "Cancelled"
            ]:
                booking.room.status = "Available"

            booking.room.save()

            messages.success(
                request,
                "Booking updated successfully."
            )

            return redirect("booking_list")

    else:

        form = BookingForm(instance=booking)

    return render(
        request,
        "bookings/booking_form.html",
        {
            "form": form,
            "title": "Update Booking"
        }
    )

@login_required
def delete_booking(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk
    )
    booking_id = booking.id

    if request.method == "POST":

        room = booking.room
        send_cancel_email(booking)
        booking.delete()
        create_log(
            request,
            "DELETE",
            "Booking",
            f"Booking {booking_id} deleted.",
            booking_id,
        )

        room.status = "Available"
        room.save()

        messages.success(
            request,
            "Booking cancelled successfully."
        )

        return redirect("booking_list")

    return render(
        request,
        "bookings/booking_confirm_delete.html",
        {
            "booking": booking
        }
    )