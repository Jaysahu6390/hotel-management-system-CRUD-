from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import RoomForm
from django.core.paginator import Paginator
from .models import Room
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from audit.utils import create_log

@login_required
def create_room(request):

    if request.method == "POST":

        form = RoomForm(request.POST, request.FILES)

        if form.is_valid():
            
            room =form.save()

            create_log(
                request,
                "CREATE",
                "Room",
                f"Room {room.room_number} created.",
                room.id
            )

            messages.success(request, "Room added successfully.")

            return redirect("room_list")

    else:

        form = RoomForm()

    return render(request, "rooms/room_form.html", {
        "form": form,
        "title": "Add Room"
    })

@login_required
def room_list(request):
    search = request.GET.get("search")

    rooms = Room.objects.all().order_by("room_number")

    if search:
        rooms = rooms.filter(
        Q(room_number__icontains=search) |
        Q(room_type__icontains=search)
        )

    paginator = Paginator(rooms, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
    }

    return render(
        request,
        "rooms/room_list.html",
        context
    )

@login_required
def update_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        form = RoomForm(
            request.POST,
            request.FILES,
            instance=room
        )

        if form.is_valid():
            room= form.save()

            create_log(
                request,
                "UPDATE",
                "Room",
                f"Room {room.room_number} updated.",
                room.id
            )
            messages.success(
                request,
                "Room updated successfully."
            )

            return redirect("room_list")

    else:
        form = RoomForm(instance=room)

    context = {
        "form": form,
        "title": "Update Room",
        "room": room,
    }

    return render(
        request,
        "rooms/room_form.html",
        context
    )

@login_required
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room_number = room.room_number
    if request.method == "POST":
        room.delete()

        create_log(
            request,
            "DELETE",
            "Room",
            f"Room {room_number} deleted.",
            pk
        )

        messages.success(
            request,
            "Room deleted successfully."
        )

        return redirect("room_list")

    return render(
        request,
        "rooms/room_confirm_delete.html",
        {
            "room": room
        }
    )