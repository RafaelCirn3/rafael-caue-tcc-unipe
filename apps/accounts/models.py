from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    school_name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    xp = models.IntegerField(default=0)
    avatar = models.URLField(blank=True)
    financial_goal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    preferences = models.JSONField(default=dict, blank=True)
    financial_profile = models.JSONField(default=dict, blank=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email or self.username
