from django.db import models
from django.conf import settings
from regions.models import Region, Place
from projects.models import Project


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks'
    )

    class Status(models.TextChoices):
        NEW = 'new', 'חדשה'
        IN_PROGRESS = 'in_progress', 'בטיפול'
        WAITING_APPROVAL = 'waiting_approval', 'ממתינה לאישור'
        COMPLETED = 'completed', 'הושלמה'
        CANCELLED = 'cancelled', 'מבוטלת'

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.NEW
    )

    class Priority(models.TextChoices):
        LOW = 'low', 'נמוכה'
        MEDIUM = 'medium', 'בינונית'
        HIGH = 'high', 'גבוהה'

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    due_date = models.DateField(null=True, blank=True)
    drive_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title