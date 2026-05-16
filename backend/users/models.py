from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'מנהל מערכת'
        HQ_MANAGER = 'hq_manager', 'מנהל מטה'
        REGION_MANAGER = 'region_manager', 'מנהל אזור'
        EMPLOYEE = 'employee', 'עובד'

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.EMPLOYEE
    )

    phone = models.CharField(max_length=20, blank=True)
    is_active_worker = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name() or self.username 
    