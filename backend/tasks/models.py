from django.db import models
from django.conf import settings
from projects.models import Project
from regions.models import Region
from places.models import Place  # הכתובת החדשה של המקומות

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
        blank=True,
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

    # ✅ השדות שהיו חסרים לניהול תוכן הוספו לכאן!
    is_content_task = models.BooleanField(default=False)
    task_type = models.CharField(max_length=50, blank=True, null=True)
    content_type = models.CharField(max_length=50, blank=True, null=True)
    content_created = models.BooleanField(default=False)

    due_date = models.DateField(null=True, blank=True)
    drive_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProjectTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='project_specific_tasks'
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_project_specific_tasks'
    )

    status = models.CharField(
        max_length=30,
        choices=Task.Status.choices,
        default=Task.Status.NEW
    )

    # ✅ השדות הוספו גם למשימות פרויקט ליתר ביטחון
    is_content_task = models.BooleanField(default=False)
    task_type = models.CharField(max_length=50, blank=True, null=True)
    content_type = models.CharField(max_length=50, blank=True, null=True)
    content_created = models.BooleanField(default=False)

    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title