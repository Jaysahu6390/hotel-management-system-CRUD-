from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.customer_list,
        name="customer_list"
    ),

    path(
        "add/",
        views.create_customer,
        name="create_customer"
    ),

    path(
        "update/<int:pk>/",
        views.update_customer,
        name="update_customer"
    ),

    path(
        "delete/<int:pk>/",
        views.delete_customer,
        name="delete_customer"
    ),


]