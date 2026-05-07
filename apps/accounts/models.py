from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    school_name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    xp = models.IntegerField(default=0)
# Create your models here.
