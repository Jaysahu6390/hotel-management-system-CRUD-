from rest_framework import viewsets
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from rooms.models import Room
from customers.models import Customer
from bookings.models import Booking
from payments.models import Payment

from .permissions import (
    RoomPermission,
    BookingPermission,
    CustomerPermission,
    PaymentPermission,
)

from .serializers import (
    RoomSerializer,
    CustomerSerializer,
    BookingSerializer,
    PaymentSerializer,
)

class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()

    serializer_class = RoomSerializer

    permission_classes = [RoomPermission]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "room_type",
        "status",
    ]

    search_fields = [
        "room_number",
        "room_type",
    ]

    ordering_fields = [
        "price",
        "room_number",
    ]

    ordering = [
        "room_number",
    ]


class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()

    serializer_class = CustomerSerializer

    permission_classes = [CustomerPermission]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "gender",
    ]

    search_fields = [
        "full_name",
        "email",
        "phone",
    ]

    ordering_fields = [
        "full_name",
    ]

class BookingViewSet(viewsets.ModelViewSet):

    queryset = Booking.objects.select_related("customer","room",)

    serializer_class = BookingSerializer

    permission_classes = [BookingPermission]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "booking_status",
        "check_in",
        "check_out",
    ]

    search_fields = [
        "customer__full_name",
        "room__room_number",
    ]

    ordering_fields = [
        "check_in",
        "check_out",
    ]


class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.select_related("booking","booking__customer",)

    serializer_class = PaymentSerializer

    permission_classes = [PaymentPermission]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "payment_method",
        "payment_status",
    ]

    search_fields = [
        "invoice_number",
        "booking__customer__full_name",
    ]

    ordering_fields = [
        "payment_date",
        "amount",
    ]