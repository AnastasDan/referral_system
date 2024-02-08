from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from referrals.models import Referral, ReferralCode
from users.models import User

from .permissions import OwnerOnlyPermission
from .serializers import (
    EmailSerializer,
    ReferralCodeSerializer,
    ReferralSerializer,
    UserSerializer,
)
from .utils import generate_referral_code


class CustomUserViewSet(viewsets.ModelViewSet):
    """Пользовательский ViewSet для взаимодействия с моделью User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (OwnerOnlyPermission,)

    @action(detail=True, methods=("get",), url_path="referrals")
    def get_referrals(self, request, pk=None):
        """Возвращает список рефералов пользователя."""
        user = get_object_or_404(User, pk=pk)
        referrals = Referral.objects.filter(referrer=user)
        if not referrals.exists():
            return Response(
                {"error": "Рефералов нет"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReferralCodeAPIView(APIView):
    """API-представление для работы с реферальными кодами пользователей."""

    serializer_class = ReferralCodeSerializer

    def get(self, request, *args, **kwargs):
        """Возвращает реферальный код пользователя."""
        cache_key = f"referral_code:{request.user.id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            print('Да')
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            referral_code = ReferralCode.objects.get(user=request.user)
            serializer = self.serializer_class(referral_code)
            data = serializer.data
            cache.set(cache_key, data, timeout=300)
            return Response(data, status=status.HTTP_200_OK)

        except ReferralCode.DoesNotExist:
            return Response(
                {"detail": "У вас нет активного реферального кода."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, *args, **kwargs):
        """Создает новый реферальный код для пользователя."""
        if ReferralCode.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "У вас уже есть активный реферальный код."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            expiry_date = timezone.now() + timezone.timedelta(days=30)
            serializer = self.serializer_class(
                data={"code": generate_referral_code()}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, expiration_date=expiry_date)

            cache_key = f"referral_code:{request.user.id}"
            cache.set(cache_key, serializer.data, timeout=300)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, *args, **kwargs):
        """Удаляет реферальный код пользователя."""
        try:
            referral_code = ReferralCode.objects.get(user=request.user)
            referral_code.delete()

            cache_key = f"referral_code:{request.user.id}"
            cache.delete(cache_key)

            return Response(
                {"detail": "Реферальный код удален."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ReferralCode.DoesNotExist:
            return Response(
                {"detail": "У вас нет активного реферального кода."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["POST"])
@permission_classes((AllowAny,))
def send_code(request):
    """Отправляет реферальный код пользователю по электронной почте."""
    try:
        data = request.data
        serializer = EmailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data.get("email")

        if not User.objects.filter(email=user_email).exists():
            return Response(
                "Почта не зарегистрирована!", status=status.HTTP_404_NOT_FOUND
            )

        if code := ReferralCode.objects.filter(user__email=user_email).first():
            try:
                send_mail(
                    subject="Ваш реферальный код",
                    message=code.code,
                    from_email="admin@admin.ru",
                    recipient_list=[user_email],
                )
                return Response(
                    "Реферальный код отправлен на вашу почту",
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    f"Ошибка при отправке письма {e}",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                "У вас нет кода", status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            f"Внутренняя ошибка сервера {e}",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
