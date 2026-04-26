from django.db import models
from django.conf import settings
from regions.models import Region, Place


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_projects'
    )

    class Status(models.TextChoices):
        PLANNED = 'planned', 'מתוכנן'
        ACTIVE = 'active', 'פעיל'
        ON_HOLD = 'on_hold', 'בהמתנה'
        COMPLETED = 'completed', 'הושלם'
        CANCELLED = 'cancelled', 'מבוטל'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    drive_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name