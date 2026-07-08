from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_number',
        'room_type',
        'price',
        'capacity',
        'floor',
        'status',
    )

    list_filter = (
        'room_type',
        'status',
        'floor',
    )

    search_fields = (
        'room_number',
        'room_type',
    )

    ordering = ('room_number',)