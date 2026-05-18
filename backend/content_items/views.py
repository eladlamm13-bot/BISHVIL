from rest_framework import viewsets
from .models import ContentItem
from .serializers import ContentItemSerializer

class ContentItemViewSet(viewsets.ModelViewSet):
    queryset = ContentItem.objects.all().order_by('-created_at')
    serializer_class = ContentItemSerializer