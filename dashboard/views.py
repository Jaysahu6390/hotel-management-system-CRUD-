from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from payments.models import Payment
from rooms.models import Room
from customers.models import Customer
from bookings.models import Booking
from audit.models import AuditLog

@login_required
def dashboard(request):

    today = timezone.now().date()

    total_rooms = Room.objects.count()

    available_rooms = Room.objects.filter(
        status="Available"
    ).count()

    occupied_rooms = Room.objects.filter(
        status="Occupied"
    ).count()
    occupancy_rate = 0
    if total_rooms:
        occupancy_rate = round(
            occupied_rooms * 100 / total_rooms,
            2
        )

    total_customers = Customer.objects.count()

    total_bookings = Booking.objects.count()

    today_checkins = Booking.objects.filter(
        check_in=today
    ).count()

    today_checkouts = Booking.objects.filter(
        check_out=today
    ).count()

    pending_payments = Booking.objects.filter(
        payment_status="Pending"
    ).count()

    total_revenue = Payment.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    top_customers = (
    Customer.objects
    .annotate(
        total_bookings=Count("booking")
    )
    .order_by("-total_bookings")[:5]
    )

    recent_bookings = Booking.objects.select_related("customer","room").order_by("-created_at")[:10]

    monthly_revenue = (
    Payment.objects
    .annotate(month=TruncMonth("payment_date"))
    .values("month")
    .annotate(total=Sum("amount"))
    .order_by("month")
    )
    todays_logins = AuditLog.objects.filter(
        action="LOGIN",
        created_at__date=today,
    ).count()

    failed_logins = AuditLog.objects.filter(
        action="FAILED_LOGIN",
        created_at__date=today,
    ).count()

    room_updates = AuditLog.objects.filter(
        action="UPDATE",
        module="Room",
    ).count()

    booking_updates = AuditLog.objects.filter(
        action="UPDATE",
        module="Booking",
    ).count()


    context = {

        "total_rooms": total_rooms,

        "available_rooms": available_rooms,

        "occupied_rooms": occupied_rooms,

        "occupancy_rate": occupancy_rate,

        "total_customers": total_customers,

        "total_bookings": total_bookings,

        "today_checkins": today_checkins,

        "today_checkouts": today_checkouts,

        "pending_payments": pending_payments,

        "total_revenue": total_revenue,

        "monthly_revenue": monthly_revenue,

        "top_customers": top_customers,

        "recent_bookings": recent_bookings,

        "todays_logins": todays_logins,

        "failed_logins": failed_logins,

        "room_updates": room_updates,

        "booking_updates": booking_updates,

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )