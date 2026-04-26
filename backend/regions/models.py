from django.db import models
from django.conf import settings


class Region(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_regions'
    )

    drive_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='places'
    )

    address = models.CharField(max_length=255, blank=True)
    drive_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.region.name}"