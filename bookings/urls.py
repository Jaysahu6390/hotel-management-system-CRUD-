from django.urls import path
from . import views

urlpatterns = [
    path("", views.booking_list, name="booking_list"),
    path("add/", views.create_booking, name="create_booking"),
    path("update/<int:pk>/", views.update_booking, name="update_booking"),
    path("delete/<int:pk>/", views.delete_booking, name="delete_booking"),
]