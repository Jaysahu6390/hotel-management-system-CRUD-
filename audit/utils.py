from .models import AuditLog


def create_log(
    request,
    action,
    module,
    description,
    object_id=None,
):

    ip = request.META.get("REMOTE_ADDR")

    AuditLog.objects.create(
        user=request.user,
        action=action,
        module=module,
        description=description,
        object_id=object_id,
        ip_address=ip,
    )