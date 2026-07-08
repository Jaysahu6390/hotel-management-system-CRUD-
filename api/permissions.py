from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Admin").exists()
        )


class IsManager(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Manager").exists()
        )


class IsReceptionist(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(
                name="Receptionist"
            ).exists()
        )


class IsHousekeeping(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(
                name="Housekeeping"
            ).exists()
        )
    




class RoomPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        # Admin
        if request.user.groups.filter(name="Admin").exists():
            return True

        # Receptionist can only view rooms
        if request.user.groups.filter(
            name="Receptionist"
        ).exists():

            return request.method in SAFE_METHODS

        # Housekeeping can view and update rooms
        if request.user.groups.filter(
            name="Housekeeping"
        ).exists():

            return request.method in [
                "GET",
                "PUT",
                "PATCH",
            ]

        return False
    

class BookingPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name="Admin").exists():
            return True

        if request.user.groups.filter(
            name="Manager"
        ).exists():

            return request.method in SAFE_METHODS

        if request.user.groups.filter(
            name="Receptionist"
        ).exists():

            return True

        return False
    
class CustomerPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name="Admin").exists():
            return True

        if request.user.groups.filter(
            name="Receptionist"
        ).exists():

            return True

        if request.user.groups.filter(
            name="Manager"
        ).exists():

            return request.method in SAFE_METHODS

        return False
    
class PaymentPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name="Admin").exists():
            return True

        if request.user.groups.filter(
            name="Manager"
        ).exists():

            return True

        if request.user.groups.filter(
            name="Receptionist"
        ).exists():

            return True

        return False