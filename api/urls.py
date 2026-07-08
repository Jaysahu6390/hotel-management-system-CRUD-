from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RoomViewSet,
    CustomerViewSet,
    BookingViewSet,
    PaymentViewSet,
)

router = DefaultRouter()

router.register(r"rooms", RoomViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"bookings", BookingViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [

    # CRUD APIs
    path("", include(router.urls)),

    # JWT Authentication
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

]