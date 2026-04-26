from django.db import models
from django.conf import settings
from tasks.models import Task
from projects.models import Project
from content_items.models import ContentItem


class Reminder(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    remind_at = models.DateTimeField()

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reminders'
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reminders'
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reminders'
    )

    content_item = models.ForeignKey(
        ContentItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reminders'
    )

    is_done = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title