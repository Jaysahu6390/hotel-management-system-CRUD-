from django.shortcuts import render, redirect

from django.contrib.auth import login

from django.contrib.auth.forms import AuthenticationForm

from .forms import RegisterForm


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("dashboard")

    else:

        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            login(request, form.get_user())

            return redirect("dashboard")

    else:

        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})