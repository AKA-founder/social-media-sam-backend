from __future__ import annotations
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Membership(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    level = models.CharField(max_length=100, blank=True, default="")   # fx "pro", "basic" eller PMPro level name/ID
    active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.email} ({'active' if self.active else 'inactive'})"
