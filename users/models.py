from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    tg_chat_id = models.CharField(
        max_length=50, verbose_name="Telegram ID", blank=True, null=True
    )
