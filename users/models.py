from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', _('SuperAdmin')
        ADMIN = 'ADMIN', _('Admin')
        USER = 'USER', _('User')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
    assigned_admin = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': Role.ADMIN},
        related_name='assigned_users'
    )

    def get_role_display(self):
        return dict(self.Role.choices)[self.role]

    def __str__(self):
        return f"{self.username} ({self.role})"