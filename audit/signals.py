from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
)
from django.dispatch import receiver

from .models import AuditLog


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):

    AuditLog.objects.create(
        user=user,
        action="LOGIN",
        module="Authentication",
        description="User logged in.",
        ip_address=request.META.get("REMOTE_ADDR"),
    )


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):

    AuditLog.objects.create(
        user=user,
        action="LOGOUT",
        module="Authentication",
        description="User logged out.",
        ip_address=request.META.get("REMOTE_ADDR"),
    )