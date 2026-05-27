from rest_framework import viewsets, filters
from .models import ContentItem
from .serializers import ContentItemSerializer
from django.db.models import Q

class ContentItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet לניהול תכנים עם סינון דינמי מול ה-Frontend
    """
    serializer_class = ContentItemSerializer

    def get_queryset(self):
        # מתחילים עם כל התוכן וממיינים לפי התאריך הכי חדש
        queryset = ContentItem.objects.all().order_by('-created_at')
        
        # תפיסת הפרמטרים שהריאקט שולח (למשל: ?region_id=1)
        region_id = self.request.query_params.get('region_id')
        place_id = self.request.query_params.get('place_id')
        project_id = self.request.query_params.get('project_id')
        content_type = self.request.query_params.get('content_type')
        approval_status = self.request.query_params.get('approval_status')
        search_query = self.request.query_params.get('search')

        # סינון דינמי לפי מה שהגיע מהריאקט
        if region_id:
            queryset = queryset.filter(region_id=region_id)
        
        if place_id:
            queryset = queryset.filter(place_id=place_id)
            
        if project_id:
            queryset = queryset.filter(associated_project_id=project_id)
            
        if content_type:
            queryset = queryset.filter(content_type=content_type)
            
        if approval_status:
            queryset = queryset.filter(approval_status=approval_status)
            
        # סינון חופשי לפי טקסט (חיפוש בכותרת או בתיאור)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        return queryset