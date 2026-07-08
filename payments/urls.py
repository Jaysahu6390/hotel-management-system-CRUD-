from django.urls import path
from . import views

urlpatterns = [
    path("", views.payment_list, name="payment_list"),
    path("add/", views.create_payment, name="create_payment"),
    path("update/<int:pk>/", views.update_payment, name="update_payment"),
    path("delete/<int:pk>/", views.delete_payment, name="delete_payment"),
    path("invoice/<int:pk>/", views.generate_invoice, name="generate_invoice"),
]