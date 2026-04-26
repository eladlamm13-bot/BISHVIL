from django.db import models
from django.conf import settings
from tasks.models import Task


class ContentItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='contents'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_contents'
    )

    class ContentType(models.TextChoices):
        IMAGE = 'image', 'תמונה'
        VIDEO = 'video', 'וידאו'
        TEXT = 'text', 'טקסט'
        LINK = 'link', 'קישור'

    content_type = models.CharField(
        max_length=20,
        choices=ContentType.choices
    )

    file_url = models.URLField(blank=True)
    drive_link = models.URLField(blank=True)

    class ApprovalStatus(models.TextChoices):
        DRAFT = 'draft', 'טיוטה'
        IN_REVIEW = 'in_review', 'בסקירה'
        APPROVED = 'approved', 'מאושר להפצה'
        REJECTED = 'rejected', 'נדחה'
        PUBLISHED = 'published', 'פורסם'

    approval_status = models.CharField(
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.DRAFT
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_contents'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title