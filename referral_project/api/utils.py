import random
import string

from django.conf import settings

import requests

from referrals.models import ReferralCode


def generate_referral_code(length=8):
    """
    Генерирует случайный уникальный реферальный код указанной длины.
    """
    characters = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choice(characters) for _ in range(length))
        if not ReferralCode.objects.filter(code=code).exists():
            return code


def verify_email(email: str):
    """Проверяет действительность email-адреса."""
    base_url = settings.EMAILHUNTER_BASE_URL
    api_key = settings.EMAIL_VERIFIER_API_KEY
    url = f"{base_url}/email-verifier?email={email}&api_key={api_key}"
    response = requests.get(url)

    data = response.json()
    if response.status_code == 200:
        if data["data"]["result"] == "deliverable":
            return True
        else:
            return False
    return False
