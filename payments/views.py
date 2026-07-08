from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,Image,
)
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from .models import Payment
from .forms import PaymentForm
from audit.utils import create_log
from core.email_service import send_payment_email
from decimal import Decimal


@login_required
def create_payment(request):

    if request.method == "POST":

        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save()
            booking = payment.booking
            booking.payment_status = "Paid"
            booking.save()

            send_payment_email(payment)
            
            create_log(
                request,
                "CREATE",
                "Payment",
                f"Payment recorded for Booking {payment.booking.id}.",
                payment.id
            )
            
            messages.success(
                request,
                "Payment recorded successfully."
            )

            return redirect("payment_list")

    else:

        form = PaymentForm()

    return render(
        request,
        "payments/payment_form.html",
        {
            "form": form,
            "title": "Record Payment",
        },
    )


@login_required
def payment_list(request):

    payments = Payment.objects.select_related(
        "booking",
        "booking__customer",
        "booking__room",
    ).order_by("-payment_date")

    paginator = Paginator(payments, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "payments/payment_list.html",
        {
            "page_obj": page_obj,
        },
    )


@login_required
def update_payment(request, pk):

    payment = get_object_or_404(
        Payment,
        pk=pk
    )

    if request.method == "POST":

        form = PaymentForm(
            request.POST,
            instance=payment
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Payment updated successfully."
            )

            return redirect("payment_list")

    else:

        form = PaymentForm(
            instance=payment
        )

    return render(
        request,
        "payments/payment_form.html",
        {
            "form": form,
            "title": "Update Payment",
        },
    )


@login_required
def delete_payment(request, pk):

    payment = get_object_or_404(
        Payment,
        pk=pk
    )

    if request.method == "POST":

        payment.delete()

        messages.success(
            request,
            "Payment deleted successfully."
        )

        return redirect("payment_list")

    return render(
        request,
        "payments/payment_confirm_delete.html",
        {
            "payment": payment,
        },
    )


def generate_invoice(request, pk):

    payment = get_object_or_404(
        Payment,
        pk=pk
    )

    booking = payment.booking

    customer = booking.customer

    room = booking.room

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="{payment.invoice_number}.pdf"'

    doc = SimpleDocTemplate(
        response,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>HOTEL MANAGEMENT SYSTEM</b>",
            styles["Title"],
        )
    )

    elements.append(
        Paragraph(
            "123 Hotel Street, Mumbai, India",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 0.25 * inch))

    elements.append(
        Paragraph(
            f"<b>Invoice No:</b> {payment.invoice_number}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Payment Date:</b> {payment.payment_date}",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 0.20 * inch))
    
    elements.append(
        Paragraph(
            "<b>Customer Details</b>",
            styles["Heading2"]
        )
    )

    customer_data = [

        ["Name", customer.full_name],

        ["Email", customer.email],

        ["Phone", customer.phone],

    ]

    table = Table(customer_data)

    table.setStyle(

        TableStyle([

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

        ])

    )

    elements.append(table)

    elements.append(Spacer(1, 0.20 * inch))

    elements.append(

        Paragraph(

            "<b>Booking Details</b>",

            styles["Heading2"]

        )

    )

    booking_table = [

        ["Room", room.room_number],

        ["Room Type", room.room_type],

        ["Check In", str(booking.check_in)],

        ["Check Out", str(booking.check_out)],

    ]

    table = Table(booking_table)

    table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

        ])

    )

    elements.append(table)


    gst = payment.amount * Decimal("0.18")

    grand_total = payment.amount + gst

    payment_table = [

        ["Room Charges", f"₹ {payment.amount}"],

        ["GST (18%)", f"₹ {gst:.2f}"],

        ["Grand Total", f"₹ {grand_total:.2f}"],

    ]

    elements.append(

        Spacer(1,0.30*inch)

    )

    elements.append(

        Paragraph(

            "<b>Payment Summary</b>",

            styles["Heading2"]

        )

    )

    table = Table(payment_table)

    table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,2),(-1,2),colors.lightblue),

        ])

    )

    elements.append(table)


    elements.append(

        Spacer(1,0.30*inch)

    )

    elements.append(

        Paragraph(

            "Thank you for staying with us.",

            styles["Heading3"]

        )

    )

    elements.append(

        Paragraph(

            "Visit Again!",

            styles["Normal"]

        )

    )

    doc.build(elements)

    logo = Image(
        "media/logo.png",
        width=80,
        height=80,
    )

    elements.insert(0, logo)

    return response