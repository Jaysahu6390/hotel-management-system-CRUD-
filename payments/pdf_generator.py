from io import BytesIO
from .models import Payment
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from decimal import Decimal
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch


def generate_invoice_pdf(booking):

    customer = booking.customer
    room = booking.room
    payment = Payment.objects.filter(
        booking=booking
    ).first()
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    elements = []


    # Logo
    logo = Image(
        "media/logo.png",
        width=80,
        height=80,
    )

    elements.append(logo)


    elements.append(
        Paragraph(
            "<b>HOTEL MANAGEMENT SYSTEM</b>",
            styles["Title"],
        )
    )

    elements.append(
        Paragraph(
            "123 Hotel Street, Kanpur, India",
            styles["Normal"],
        )
    )

    elements.append(
        Spacer(1, 0.25 * inch)
    )


    elements.append(
        Paragraph(
            f"<b>Invoice No:</b> {payment.invoice_number if payment else 'Not Generated'}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Payment Date:</b> {payment.payment_date if payment else 'Pending'}",
            styles["Normal"],
        )
    )


    elements.append(
        Spacer(1, 0.20 * inch)
    )


    # Customer Details

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

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

        ])
    )

    elements.append(table)


    elements.append(
        Spacer(1,0.20*inch)
    )


    # Booking Details

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



    # Payment Summary
    amount = payment.amount if payment else 0
    gst = payment.amount * Decimal("0.18")

    grand_total = payment.amount + gst


    elements.append(
        Spacer(1,0.30*inch)
    )


    elements.append(
        Paragraph(
            "<b>Payment Summary</b>",
            styles["Heading2"]
        )
    )


    payment_table = [

        ["Room Charges", f"₹ {amount:.2f}"],

        ["GST (18%)", f"₹ {gst:.2f}"],

        ["Grand Total", f"₹ {grand_total:.2f}"],

    ]


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


    # Generate PDF
    doc.build(elements)


    pdf = buffer.getvalue()

    buffer.close()


    return pdf

