from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, username, email, first_name, last_name, role, password=None, **extra_fields):
        if not username:
            raise ValueError("User must provide Username")
        if not email:
            raise ValueError("User must provide Email")
        if not role:
            raise ValueError("User must provide Role")

        user = self.model(username=username, email=self.normalize_email(email), first_name=first_name, last_name=last_name, role=role, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, username, email, first_name, last_name, role, password=None, **extra_fields):
        if not username:
            raise ValueError("User must provide Username")
        if not email:
            raise ValueError("User must provide Email")

        super_user = self.model(username=username, email=self.normalize_email(email), first_name=first_name, last_name=last_name, role=role, **extra_fields)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.set_password(password)
        super_user.save()

        return super_user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    slack_access_token = models.CharField(max_length=255, blank=True, null=True)
    slack_user_id = models.CharField(max_length=255, blank=True, null=True)
    slack_team_id = models.CharField(max_length=255, blank=True, null=True)
    slack_channel_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role', 'first_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def token(self):
        refresh_token = RefreshToken.for_user(self)

        return {
            'access_token': str(refresh_token.access_token),
            'refresh_token': str(refresh_token)
        }