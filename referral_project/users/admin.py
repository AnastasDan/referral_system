from django.contrib import admin

from .models import User

admin.site.empty_value_display = "Не задано"


@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    """Административная панель для управления пользователями."""

    list_display = ("username", "first_name", "last_name", "email")
    list_filter = ("username", "email")
    search_fields = ("username",)
