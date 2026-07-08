from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path("add/",views.create_room,name="create_room"),
    path("update/<int:pk>/",views.update_room,name="update_room"),
    path("delete/<int:pk>/",views.delete_room,name="delete_room"),
]