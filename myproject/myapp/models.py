from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Allow blank username initially
    reg_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=191, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255, default="")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True, auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.username:  # Set username if not provided
            self.username = self.reg_number  # Use reg number as username
        if self.is_admin:
            self.is_superuser = True
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
