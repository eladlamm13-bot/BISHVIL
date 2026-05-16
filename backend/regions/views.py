from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Region
from .serializers import RegionSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]

# ה-PlaceViewSet נמחק מכאן כי הוא כבר קיים בתיקיית places/views.py