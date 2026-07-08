from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Customer
from .forms import CustomerForm
from audit.utils import create_log


@login_required
def create_customer(request):

    if request.method == "POST":

        form = CustomerForm(
            request.POST
        )

        if form.is_valid():

            customer = form.save()
            create_log(
                request,
                "CREATE",
                "Customer",
                f"Customer {customer.full_name} created.",
                customer.id
            )

            messages.success(
                request,
                "Customer added successfully."
            )

            return redirect("customer_list")

    else:

        form = CustomerForm()

    context = {

        "form": form,

        "title": "Add Customer"

    }

    return render(
        request,
        "customers/customer_form.html",
        context
    )


@login_required
def customer_list(request):

    search = request.GET.get("search", "")

    customers = Customer.objects.all().order_by("full_name")

    if search:
        customers = customers.filter(
            Q(full_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    paginator = Paginator(customers, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
    }

    return render(
        request,
        "customers/customer_list.html",
        context
    )


@login_required
def update_customer(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    if request.method == "POST":

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():

            customer = form.save()

            create_log(
                request,
                "UPDATE",
                "Customer",
                f"Customer {customer.full_name} updated.",
                customer.id
            )

            messages.success(
                request,
                "Customer updated successfully."
            )

            return redirect(
                "customer_list"
            )

    else:

        form = CustomerForm(
            instance=customer
        )

    context = {

        "form": form,

        "title": "Update Customer",

        "customer": customer,

    }

    return render(
        request,
        "customers/customer_form.html",
        context
    )

@login_required
def delete_customer(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk
    )
    name = customer.full_name

    if request.method == "POST":

        customer.delete()
        create_log(
            request,
            "DELETE",
            "Customer",
            f"Customer {name} deleted.",
            pk
        )

        messages.success(
            request,
            "Customer deleted successfully."
        )

        return redirect("customer_list")

    return render(
        request,
        "customers/customer_confirm_delete.html",
        {
            "customer": customer
        }
    )