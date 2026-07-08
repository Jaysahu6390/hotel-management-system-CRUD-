from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):

    ACTIONS = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("FAILED_LOGIN", "Failed Login"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=20,
        choices=ACTIONS,
        default="CREATE",
    )

    module = models.CharField(max_length=50)

    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    description = models.TextField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.action}"