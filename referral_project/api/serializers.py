from django.core.cache import cache
from django.utils import timezone

from rest_framework import serializers

from referrals.models import Referral, ReferralCode
from users.models import User

from .utils import verify_email


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    """

    referral_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "referral_code",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Создает нового пользователя на основе предоставленных данных."""
        referral_code_str = validated_data.pop("referral_code", None)

        email = validated_data.get("email")
        if not verify_email(email):
            raise serializers.ValidationError(
                {"error": f"Указанный email '{email}' не прошел проверку"}
            )

        if referral_code_str:
            cache_key = f"referral_code_validity:{referral_code_str}"
            cached_data = cache.get(cache_key)

            if cached_data is None or cached_data is False:
                try:
                    referral_code = ReferralCode.objects.get(
                        code=referral_code_str,
                        expiration_date__gte=timezone.now(),
                    )
                    cache.set(cache_key, True, timeout=300)
                except ReferralCode.DoesNotExist:
                    cache.set(cache_key, False, timeout=300)
                    raise serializers.ValidationError(
                        {
                            "error": "Недействительный или истекший код"
                        }
                    )

                user = User.objects.create_user(**validated_data)
                Referral.objects.create(
                    referrer=referral_code.user, referred=user
                )
            else:
                raise serializers.ValidationError(
                    {"error": "Недействительный или истекший реферальный код"}
                )
        else:
            user = User.objects.create_user(**validated_data)

        return user


class ReferralCodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели реферального кода.
    """

    expiry_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", source="expiration_date", read_only=True
    )

    class Meta:
        model = ReferralCode
        fields = (
            "code",
            "expiry_date",
        )


class ReferralSerializer(serializers.ModelSerializer):
    """Сериализатор для модели реферала."""

    referred_username = serializers.ReadOnlyField(source="referred.username")
    referred_email = serializers.ReadOnlyField(source="referred.email")
    referral_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", source="created_at", read_only=True
    )

    class Meta:
        model = Referral
        fields = (
            "referred_username",
            "referred_email",
            "referral_date",
        )


class EmailSerializer(serializers.Serializer):
    """Сериализатор для проверки валидности электронной почты."""

    email = serializers.EmailField()

    class Meta:
        fields = ("email",)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Данная почта не зарегистрирована."
            )
        return email
