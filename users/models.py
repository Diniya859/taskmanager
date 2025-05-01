from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('SUPERADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return self.username

    @property
    def is_superadmin(self):
        return self.role == 'SUPERADMIN'

    @property
    def is_admin(self):
        return self.role == 'ADMIN'

    @property
    def is_user(self):
        return self.role == 'USER'