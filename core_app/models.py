from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class User(AbstractUser):
    profile_id = models.UUIDField(
        default=uuid.uuid4, null=False, unique=True, primary_key=True, blank=True)

class EmailInfo(models.Model):
    info_id = models.UUIDField(
        default=uuid.uuid4, null=False, unique=True, primary_key=True, blank=True)
    platform = models.CharField(
        max_length=20, default="", null=False, blank=False)
    first_name = models.CharField(
        max_length=20, default="", null=False, blank=False)
    last_name = models.CharField(
        max_length=20, default="", null=False, blank=False)
    generated_email_address = models.CharField(
        max_length=30, default="", null=False, blank=False)
    generated_password = models.CharField(
        max_length=20, default="", null=False, blank=False)
    user = models.ForeignKey(User, models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
