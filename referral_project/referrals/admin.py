from django.contrib import admin

from .models import Referral, ReferralCode

admin.site.empty_value_display = "Не задано"


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Административная панель для модели Referral."""

    list_display = ("referrer", "referred", "created_at")
    search_fields = ("referrer__username", "referred__username")


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    """Административная панель для модели ReferralCode."""

    list_display = ("user", "code", "expiration_date", "created_at")
    search_fields = ("user__username", "code")
