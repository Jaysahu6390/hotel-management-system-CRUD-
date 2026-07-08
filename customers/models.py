from django.db import models


class Customer(models.Model):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,unique=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    address = models.TextField()
    nationality = models.CharField(max_length=50)
    id_proof = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name