from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, ReferralCodeAPIView, send_code

router = DefaultRouter()
router.register(r"users", CustomUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("send_code/", send_code, name="send_code"),
    path("referral_codes/", ReferralCodeAPIView.as_view()),
    path("auth/", include("djoser.urls.jwt")),
]
