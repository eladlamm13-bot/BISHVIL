from django.db import models
from regions.models import Region 

class PlaceType(models.Model):
    name = models.CharField(max_length=100)
    technical_value = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=20, default="#3A9154")
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='places')
    place_type = models.ForeignKey(PlaceType, on_delete=models.SET_NULL, null=True, blank=True, related_name='places')
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name