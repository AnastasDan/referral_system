from django.db import models

from users.constants import TEN
from users.models import User


class ReferralCode(models.Model):
    """Модель представляет собой код, привязанный к пользователю."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    code = models.CharField("Код реферрала", max_length=TEN, unique=True)
    expiration_date = models.DateTimeField("Дата истечения срока")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ("id",)
        verbose_name = "Реферальный код"
        verbose_name_plural = "Реферальные коды"

    def __str__(self):
        """Возвращает строковое представление реферального кода."""
        return self.code


class Referral(models.Model):
    """Модель представляет собой связь между реферрером и реферралом."""

    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="referrals",
        verbose_name="Реферрер",
    )
    referred = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="referrer",
        verbose_name="Реферал",
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ("id",)
        verbose_name = "Реферальная связь"
        verbose_name_plural = "Реферальные связи"

    def __str__(self):
        """Возвращает строковое представление реферальной связи."""
        return f"{self.referrer} -> {self.referred}"
