
from django.db import models
from django.core.validators import MinValueValidator
from users.models import CustomUser

class TaskStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        limit_choices_to={'role': CustomUser.Role.USER}
    )
    assigned_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        limit_choices_to={'role__in': [CustomUser.Role.ADMIN, CustomUser.Role.SUPERADMIN]}
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.title} - {self.assigned_to.username} ({self.status})"

    class Meta:
        ordering = ['-created_at']