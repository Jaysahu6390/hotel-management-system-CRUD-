from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from payments.pdf_generator import generate_invoice_pdf

def send_booking_email(booking):

    subject = "Booking Confirmation"

    context = {
        "booking": booking,
        "customer": booking.customer,
        "room": booking.room,
    }

    html_content = render_to_string(
        "emails/booking_confirmation.html",
        context,
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="Your booking has been confirmed.",
        to=[booking.customer.email],
    )

    email.attach_alternative(
        html_content,
        "text/html",
    )
    
    email.send()

def send_payment_email(payment):

    subject = "Payment Received"

    context = {
        "payment": payment,
        "booking": payment.booking,
    }

    html = render_to_string(
        "emails/payment_receipt.html",
        context,
    )

    email = EmailMultiAlternatives(
        subject,
        "",
        to=[payment.booking.customer.email],
    )

    email.attach_alternative(
        html,
        "text/html",
    )
    pdf_bytes = generate_invoice_pdf(payment.booking)

    email.attach(
        "Invoice.pdf",
        pdf_bytes,
        "application/pdf",
    )
    email.send()


def send_cancel_email(booking):

    subject = "Booking Cancelled"

    context = {
        "booking": booking,
    }

    html = render_to_string(
        "emails/booking_cancelled.html",
        context,
    )
    email = EmailMultiAlternatives(

        subject,

        "",

        to=[booking.customer.email],
    )

    email.attach_alternative(
        html,
        "text/html",
    )
    email.send()