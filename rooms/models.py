from django.db import models
class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    ]

    STATUS = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Maintenance', 'Maintenance'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Available'
    )
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='rooms/',
        blank=True,
        null=True
    )
    def __str__(self):
        return self.room_number